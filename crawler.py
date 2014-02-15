#!/usr/bin/python
import urllib
import json
import lxml
from lxml import html

def getgoogle(query):
	try:
		urllist = []
		query = urllib.urlencode({'q': query})
		url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
		for start in range(0, 10, 4):
			#request_url = '{0}&start={1}'.format(url, start)
			search_results = urllib.urlopen(url)
			json_string = json.loads(search_results.read())
			results = json_string['responseData']['results']
			for i in results:
				urllist.append(i['url'])
		return urllist
	except Exception as e:
		print 'Error in getgoogle : '+str(e)

def parser(url):
	try:
		urllist = []
		page = urllib.urlopen(url)
		content = page.read()
		html = lxml.html.fromstring(content)
		print type(html)
		urls = html.xpath('//a')
		for u in urls:
			urllist.append(u.get('href'))
		return urllist
	except Exception as e:
		print 'Error in parser : '+str(e)

def crawler(query):
	try:
		urllist = getgoogle(query)
		#for i in urllist:
			#print i
			
		#for page in urllist:
		for i in parser(urllist[0]):
			print i
		
		#print type(pagecontent.read())
	except Exception as e:
		print 'Error in crawler : '+str(e)
		

crawler('dog')
