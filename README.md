Web_Crawler
===========

------------------------------------------------------------------------

ReadMe for Web Crawler

------------------------------------------------------------------------
Files Included : 
python.py : The main program for the crawler
explain.txt : Text file containing information regarding the working of 
the crawler

------------------------------------------------------------------------
Libraries : urllib, lxml, heapq, json, math, sys, threading, robotparser
for lxml use : pip install lxml

------------------------------------------------------------------------
To Execute :
Just run the crawler.py python file. 
No need to create any other file separately. 
Extracted links will be saved in links.txt file in same directory.

------------------------------------------------------------------------
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
