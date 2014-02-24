#!/usr/bin/python
import urllib, lxml, json, sys, threading, robotparser
from sys import stdout
from threading import Thread
from heapq import *
from lxml import html
#=======================================================================
# Start of Crawler Class				
#=======================================================================
class Crawler(threading.Thread):
	#Constructor for Crawler Thread Object		
	def __init__(self, thread_id, url, query, file, lock):
		threading.Thread.__init__(self)
		self.thread_id = thread_id
		self.query = query
		self.url = url
		self.file = file
		self.lock = lock
#=======================================================================			
	# Method to check if url already visited
	# If already visited, returns back the reference to that url in the list
	# If not present, returns back an empty list
	def pagevisited(self, url):
		existing_page = []
		for q in pq:
				for r in q:
					if r == url:
						existing_page = q	
		return existing_page
#=======================================================================
	# Recursive crawl method for parsing the html content, determining
	# the word count, assigning priority, pushing elements into priority
	# queue and writing page details of relevant link to link.txt
	def crawl(self, url):
		try:
			global num_of_visited_links, pq, total_downloaded_size
			
			#Checking if the specified page limit is reached or not
			if len(pq)>total_page_limit:
				return
			
			try:
				#Extracting home link of current page to get URL/robots.txt
				rpurl = url
				if '/' in url[url.index('.'):]:
					rpurl = url[:url.index('/',url.index('.'))]
				rpurl = rpurl + '/robots.txt'
				#Checking if current url can be visited
				rp = robotparser.RobotFileParser()
				rp.set_url(rpurl)
				rp.read()
				if not rp.can_fetch("*", url):
					return
			except Exception as e:
				if debug_mode:
					print 'Error in Robot Parser : '+str(e)
				pass
			
			#Opening the url and reading its content	
			page = urllib.urlopen(url)
			content = page.read()
			#content = content[content.index("<body"):content.index("</body")]
			
			#Using lxml library to extract html from the content
			html = lxml.html.fromstring(content)
			#Modifying all relative urls present in html file and making
			#them absolute using the specified url passed as parameter
			html.make_links_absolute(url)
			
			#Incrementing the total downloaded size of all pages
			total_downloaded_size = total_downloaded_size + sys.getsizeof(content)
			
			#Incrementing no. of visited links for each page visited
			num_of_visited_links = num_of_visited_links + 1
			
			#Printing out <Links visited : __ | Relevent Links : __ >
			stdout.write("\rLinks Visited : %i | Relevant Links : %i" % (num_of_visited_links, len(pq)))
			stdout.flush()
			
			#Extracting text content
			text_content = html.text_content()

			#Calculating word count for given query
			word_count = 0
			query_words = self.query.split()
			for w in query_words:
				word_count += text_content.count(w)
				
			#If word count is less than 1; page irrelevant!	
			if word_count < 1 :
				return

			#Checking is the present url is an anchor jump url
			#If yes, then extract the parent link from anchor jump url
			#and use that as current url if not already present in the 
			#priority queue
			anchor_jump_link = ''
			if '#' in url:
				anchor_jump_link = url[:url.index('#')]
				#if self.pagevisited(anchor_jump_link):
				#	return
				#else:
				url = anchor_jump_link

			#Check to see if the page already exists or not
			#If yes, then increase the page priority by one and return
			#If not, then acquire lock and write url details onto links.txt
			#and push [priority, url] into pq (priority queue)
			existing_page = self.pagevisited(url)			
			if not existing_page:
				self.lock.acquire()
				self.file.write('Link : '+url+' | Word Count(Priority) : '+str(word_count)+'\n')
				self.lock.release()
				heappush(pq, [-word_count, url])
			else:
				existing_page[0] = existing_page[0] + (-1)
				return
				
			#Extracting all anchor tag elements	
			urls = html.xpath('//a')
			#Iterating though all anchor tags that were extracted
			for u in urls:
			#Extracting the href attribute of each anchor tag for get a url
				link = u.get('href')
				#If extracted url not already visited, converting it to 
				#lower case and passing it to crawl method recursively
				if not self.pagevisited(link):
					if issubclass(type(link), unicode) or issubclass(type(link), str):
						self.crawl(link.lower())
						
		except Exception as e:
			if debug_mode:
				print 'Error in parser : url<'+url+'> : ' + str(e)
			pass
#=======================================================================
	# Run method is executed for ever Thread.start(). Every thread 
	# creates an iterative crawl for all the urls present in the page
	# and calls Crawl method to crawl thode urls recursively
	def run(self):
		try:
			global num_of_visited_links, pq, total_downloaded_size
			
			#Checking if the specified page limit is reached or not
			if len(pq)>total_page_limit:
				return
			#Checking if the type of url is correct
			if not issubclass(type(self.url), unicode) and not issubclass(type(self.url), str):
				return
			
			#Opening the url and reading its content	
			page = urllib.urlopen(self.url)
			content = page.read()
			#content = content[content.index("<body"):content.index("</body")]
			
			#Using lxml library to extract html from the content
			html = lxml.html.fromstring(content)
			#Modifying all relative urls present in html file and making
			#them absolute using the specified url passed as parameter
			html.make_links_absolute(self.url)
			
			#Incrementing the total downloaded size of all pages
			total_downloaded_size = total_downloaded_size + sys.getsizeof(content)
			
			#Incrementing no. of visited links for each page visited
			num_of_visited_links = num_of_visited_links + 1
			
			#Printing out <Links visited : __ | Relevent Links : __ >
			#stdout.write("\rLinks Visited : %i | Relevant Links : %i" % (num_of_visited_links, len(pq)))
			#stdout.flush()
			
			#Extracting text content
			text_content = html.text_content()

			#Calculating word count for given query
			word_count = 0
			query_words = self.query.split()
			for w in query_words:
				word_count += text_content.count(w)
				
			#If word count is less than 1; page irrelevant!
			if word_count < 1 :
				return
			
			#Extracting all anchor tag elements
			urls = html.xpath('//a')
			#Iterating though all anchor tags that were extracted
			for u in urls:
				#Extracting the href attribute of each anchor tag for get a url
				link = u.get('href')
				#If extracted url not already visited, converting it to 
				#lower case and passing it to crawl method
				if not self.pagevisited(link):
					if issubclass(type(link), unicode) or issubclass(type(link), str):
						self.crawl(link.lower())
								
		except Exception as e:
			if debug_mode:
				print "Exception in Run : "+ str(e)
			pass
#=======================================================================	
# End of Crawler Class		
#=======================================================================
# GLOBAL VARIABLES

#Variable to track number of links visited
num_of_visited_links = 0
#Variable to keep track of Mbs downloaded
total_downloaded_size = 0
#Variable to keep track of total page limit
total_page_limit = 0
debug_mode = False
#Priority queue to store [priority, url]
pq = []
#=======================================================================
# Main method which controls thread creation and search url extraction
def main():
	try:
		global total_page_limit, debug_mode
		print("============================Web Crawler================================\n")
		query = raw_input("Enter a word to begin web crawl: ")
		total_page_limit = int(raw_input("Enter number of pages to crawl : "))
		debug = raw_input("\nRun code in debug mode(y/n) : ")
		if debug == 'y':
			debug_mode = True
		print("-----------------------------------------------")
		
		#Retrieving top 10 results from google
		seedurls = getgoogle(query)
		#Creating a list for storing threads
		threads = []
		#Counter to assign threadid to all threads
		threadid = 1
		#Creating a lock so that only one thread can write to a file at a given time
		lock = threading.Lock()
		#Opening/Creating file links.txt which will store the relevant links
		file = open('links.txt', 'w+')
		file.write('=======================================================================')
		file.write('\n**************************Web Crawler Results**************************')
		file.write('\n=======================================================================\n\n')
		file.write('Query : '+ query +' | Page Limit : '+ str(total_page_limit) +'\n\n')
		
		#Iterating though top 10 google search results
		for url in seedurls[:10]:
			#Creating a thread Crawler for each url
			thread = Crawler(threadid, url, query, file, lock)
			thread.start()
			threads.append(thread)
			threadid += 1
		
		#Waiting for all threads to get completed	
		for th in threads:
			th.join()
		
		print '\n\nSaving urls to links.txt'
		print '\nPercentage Accuracy : '+str(total_page_limit*100/num_of_visited_links)+'%'	
		print 'Total size of '+ str(num_of_visited_links) +' downloaded pages : ' + str(total_downloaded_size/1048576) +' Mbs ****'
		
		
		file.write('\n=======================================================================')
		file.write('\nPercentage Accuracy : '+str(total_page_limit*100/num_of_visited_links)+'%')
		file.write('\nTotal size of '+ str(num_of_visited_links) +' downloaded pages : ' + str(total_downloaded_size/1048576) +' Mbs ****')
		file.write('\n=======================================================================\n\n')
		file.close()
			
		print('\n\n=======================================================================')
		
	except Exception as e:
		if debug_mode:
			print "Exception in Main : "+str(e)
#=======================================================================
# Gets the top ten google search results for the given query. Most logic 
# for this method was adopted from a link found on www.stackoverflow.com
def getgoogle(query):
	try:
		#Empty list of seedurls
		seedurls = []
		#Encoding the query in required format
		encoded_query = urllib.urlencode({'q': query})
		#Using the googleapis link to retrieve search results
		url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % encoded_query
		#The above api returns 4 search results at a time. To get more 
		#results we iterate over the url 
		for start in range(0, 10, 4):
			request_url = '{0}&start={1}'.format(url, start)
			search_results = urllib.urlopen(request_url)
			#On opening the url, it returns back a json file which needs
			#to be parsed in order to extract search results
			json_string = json.loads(search_results.read())
			results = json_string['responseData']['results']
			#Appending the extracted urls to the seedurl list
			for i in results:
				seedurls.append(i['url'])
		return seedurls
	except Exception as e:
		if debug_mode:
			print 'Error in getgoogle : ' + str(e)
#=======================================================================	
if __name__ == "__main__":
	main()
#=======================================================================
