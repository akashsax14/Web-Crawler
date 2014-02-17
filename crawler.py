#!/usr/bin/python
import urllib
import json
import lxml
import robotparser
from heapq import *
from lxml import html

class Crawler:
	#class Page:
	#	def __init__(self, url, urllist):
	#		self.url = url
	#		self.urllist = urllist
#=======================================================================			
	def __init__(self, query, n):
		self.query = query
		self.googlelist = []
		self.urllist = []
		self.urls = []
		self.pq = []
		self.n = n
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
			global parsed_no_of_pages
			parsed_no_of_pages = parsed_no_of_pages+1
			if parsed_no_of_pages>5:
				return
			if len(self.pq)>self.n:
				return
			if not issubclass(type(url), unicode):
				return	
			#print type(url)
			page = urllib.urlopen(url)
			content = page.read()
			
			#saving word count in current page
			n = content.count(self.query)
			
			#Add url to PQ only if word count more than 0 AND url not already present
			if n <> 0 and not any(url in c for c in self.pq):
				heappush(self.pq, [-n, url])
			
			html = lxml.html.fromstring(content)
			html.make_links_absolute(url)
			urls = html.xpath('//a')
			
			for u in urls:
				link = u.get('href')
				if issubclass(type(link), str):
					#print unicode(link)
					self.parser(unicode(link))
					self.urllist.append(link)
			
			#Gives all the urls in the page
			#self.urllist = list(set(self.urllist))
			#add url to dictionary
			#self.urls[url]=n
			
		except Exception as e:
			print 'Error in parser : ' + str(e)
#=======================================================================
	def crawl(self):
		try:
			self.getgoogle()
			for url in self.googlelist[:10]:
				global parsed_no_of_pages
				parsed_no_of_pages=0
				self.parser(url)
			
			while self.pq:
				maxp=heappop(self.pq)
				maxp[0]=-maxp[0]
				print maxp
			print 'Parsed no. of pages : ' + str(parsed_no_of_pages)	
		except Exception as e:
			print 'Error in crawler : ' + str(e)
#=======================================================================		
parsed_no_of_pages=0
c=Crawler('brooklyn',20)
#=======================================================================
