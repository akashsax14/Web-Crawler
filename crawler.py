#!/usr/bin/python
import urllib
import json
import lxml
import robotparser
from heapq import *
from lxml import html

class myURLopener(urllib.FancyURLopener):
    def http_error_401(self, url, fp, errcode, errmsg, headers, data=None):
        return None
        
class Crawler:
	#class Page:
	#	def __init__(self, url, urllist):
	#		self.url = url
	#		self.urllist = urllist
#=======================================================================			
	def __init__(self, query, page_count):
		self.query = query
		self.googlelist = []
		self.urllist = []
		self.urls = []
		self.pq = []
		self.page_count = page_count
		self.crawl()
#=======================================================================
	#Gets the top ten google search results for the given query
	def getgoogle(self):
		try:
			encoded_query = urllib.urlencode({'q': self.query})
			url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % encoded_query
			for start in range(0, 10, 4):
				request_url = '{0}&start={1}'.format(url, start)
				search_results = urllib.urlopen(request_url)
				json_string = json.loads(search_results.read())
				results = json_string['responseData']['results']
				for i in results:
					self.googlelist.append(i['url'])
				#Removing duplicaties
				#self.googlelist = list(set(self.googlelist))
		except Exception as e:
			print 'Error in getgoogle : ' + str(e)
#=======================================================================
	#Parses the url given and returns the list of links present on the plage
	def parser(self, url):
		try:
			global parsed_no_of_pages, is_main_page
			parsed_no_of_pages = parsed_no_of_pages+1
			if is_main_page:
				if parsed_no_of_pages>200:
					return
			
			if len(self.pq)>self.page_count:
				return
			if not issubclass(type(url), unicode):
				return	
			
			page = urllib.urlopen(url)
			content = page.read()
			
			#saving word count in current page
			word_count = content.count(self.query)
			
			#Add url to PQ only if word count more than 0 AND url not already present
			if word_count > 0 and not any(url in queue for queue in self.pq):
				#To check if the current url is just an anchor jump variation of a url that is already present
				#Like www.wikipedia.org#bottom which is the same pages as www.wikipedia.org
				if '#' in url:
					anchor_jump = url[:url.index('#')-1]
					if not any(anchor_jump in queue for queue in self.pq):
						return
				#print str(len(self.pq))+' : '+url
				heappush(self.pq, [-word_count, url])
			else:
				return
			
			#Getting html content from the page in lxml.html format to parse content
			html = lxml.html.fromstring(content)
			html.make_links_absolute(url)
			urls = html.xpath('//a')
			
			#Iterating through all <a> tags on page
			if is_main_page:
				is_main_page=False
				for u in urls:
					#Extracting link from href attribute of <a> tag
					link = u.get('href')
					if issubclass(type(link), str):
						#Parsing the extraced link
						self.parser(unicode(link))
			
		except Exception as e:
			print 'Error in parser : ' + str(e)
#=======================================================================
	def crawl(self):
		try:
			self.getgoogle()
			for url in self.googlelist[:1]:
				global parsed_no_of_pages, is_main_page
				parsed_no_of_pages=0
				is_main_page = True
				self.parser(url)
				#print parsed_no_of_pages
			
			while self.pq:
				maxp=heappop(self.pq)
				maxp[0]=-maxp[0]
				print maxp	
		except Exception as e:
			print 'Error in crawler : ' + str(e)
#=======================================================================		
parsed_no_of_pages=0
is_main_page = True
c=Crawler('dog',20)
#=======================================================================
