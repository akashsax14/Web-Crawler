Web_Crawler
===========

A Web crawler is an Internet bot that systematically browses the World Wide Web, typically for the purpose of Web indexing. A Web crawler may also be called a Web spider, an ant, an automatic indexer, or a Web scutter. Web search engines and some other sites use Web crawling or spidering software to update their web content or indexes of others sites' web content. Web crawlers can copy all the pages they visit for later processing by a search engine that indexes the downloaded pages so that users can search them much more quickly.

This web crawler is a focused crawler which takes in a query from the user. It then get the top ten google search results and starts crawling those urls simultaneously using multithreading. For every page that is getting crawled, word occurance count is maintained and all the links are expracted from the page. These extracted links are then recursively crawled based on page relevance (ie. if query string is present on the page). A max Priority Queue is maintained to store the pages (word count as priority) for any future use for page ranking. 

All the relevant links that are extracted are saved in a file "links.txt". The accuracy of crawler is calculated along with the total quantity of data that was downloaded in Mb's. 

------------------------------------------------------------------------
1) Program Structure

class Crawler:
	def __init__(self, thread_id, url, query, file, lock):
	def pagevisited(self, url):
	def crawl(self, url):
	def run(self):

def main():
def getgoogle(query):

------------------------------------------------------------------------
2) Input Data

Query : Word/words to be searched
Page Limit Number : Number of pages that are to be retireved 

Debug Mode : Prints out the exception messages

------------------------------------------------------------------------
3) Execution

Step 1> main -> getgoogle
Step 2> main -> Crawler.start (x10) -> run
Step 3> run  -> crawl
Step 4> crawl-> crawl

Step 1>	Execution begins at the main() method which prompts the user 
	for query input and for number of pages to be found.The query 
	is then passed to getgoogle() method which returns the top 10 
	search results for the given query.

Step 2>	The main() method then iterates over each url returned by 
    	getgoogle() and creates a thread object Crawler for each url.
    	Each thread is started and the run() method is invoked for 
    	every instance of thread.

Step 3>	The run() method then parses the url passed to it and extracts
    	all links on the page. It then iterates over all the extracted
    	links and calls the crawl() method for crawling each url.

Step 4>	The crawl() method parses the url passed to it. It checks if
    	the link has already been visited or not. It then checks the
    	robots.txt file of the host url and checks if the current url
    	can be accessed. Then the word count is calculated and the 
    	url is pushed into the priority queue along with the word count
    	as page priority. ALso the crawl() method checks if the url
    	if an anchor jump link. Once the page information is written
    	onto the file links.txt, all the links on the current page 
    	are extracted. Iterating over these links, each link is
    	passed to crawl() method as a recursive call. 

The program execution continues till the specified number of pages have 
been found or till the crawler has crawler all the relevant links. Any 
exception that is thrown is ignored unless the program is running in 
debug_mode. 

Also, since there are multiple threads running, we used thread locks
while writing data onto the file since we don't want more than one 
thread writing onto the file. 

------------------------------------------------------------------------
4) Output Data

All the relevant links are saved in a file name links.txt in the same 
directory. The program also calculates the approximate amount of data 
that was downloaded and what percent of it was relevant.

------------------------------------------------------------------------
------------------------------------------------------------------------
Libraries Used : 
urllib, lxml, heapq, json, math, sys, threading, robotparser

Required library installation : 
for lxml use : pip install lxml

To Execute :
Run the crawler.py python file. 
No need to create any other file separately. 
Extracted links will be saved in links.txt file in same directory.

------------------------------------------------------------------------
