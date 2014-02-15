#!/usr/bin/python
import urllib
import json
import lxml
from lxml import html

#Gets the top ten google search results for the given query
def getgoogle(query):
	try:
		urllist = []
		query = urllib.urlencode({'q': query})
		url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
		for start in range(0, 10, 4):
			request_url = '{0}&start={1}'.format(url, start)
			search_results = urllib.urlopen(request_url)
			json_string = json.loads(search_results.read())
			results = json_string['responseData']['results']
			for i in results:
				urllist.append(i['url'])
		return urllist
	except Exception as e:
		print 'Error in getgoogle : ' + str(e)

#Parses the url given and returns the list of links present on the page
def parser(url, query):
	try:
		urllist = []
		page = urllib.urlopen(url)
		content = page.read()
		html = lxml.html.fromstring(content)
		urls = html.xpath('//a')
		for u in urls:
			urllist.append(u.get('href'))
		return urllist, content.count(query)
	except Exception as e:
		print 'Error in parser : ' + str(e)

def crawler(query):
	try:
		urllist = getgoogle(query)
		
		for page in urllist[0:10]:
			print '=============' + page + '============='
			parse_result, count = parser(page, query)
			#for i in parse_result[1:10]:
				#print i
			print count
		#print type(pagecontent.read())
	except Exception as e:
		print 'Error in crawler : ' + str(e)
		
crawler('dog')
