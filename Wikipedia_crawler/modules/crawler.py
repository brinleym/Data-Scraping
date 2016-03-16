import re #regex library
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

#this class handles the the scraping and parsing of a webpage 

#makes a request for source code
#instantiates BeautifulSoup object to parse source code
#finds and stores links on a webpage in list 
class Parser:

	def __init__(self, target_url):
		self.url = target_url
		self.links = []

	def makeRequest(self):
		try:
			response = requests.get(self.url)
			print "page okay. parsing html..."
			self.parseHtml(response)
			return True
		except ConnectionError as error:
			print error
			print "Page not found. Returning false.."
			return False

	def parseHtml(self, source_code):
		plain_text = source_code.text
		html_soup = BeautifulSoup(plain_text, "html.parser")

		if(self.isWikiPage(self.url)):
			print "Visiting wiki page.."
			self.getLinksFromWiki(html_soup)
		else:
			#get links from non-Wiki
			print "Visiting another page.."
			self.getLinksFromNonWiki(html_soup) 

	def getLinksFromWiki(self, soup):
		for link in soup.find_all("a", class_="external",
								   href=re.compile("http")):
			href = link.get("href")
			self.links.append(href)

	def getLinksFromNonWiki(self, soup):
		print "Getting links from non-Wiki.."
		for link in soup.find_all("a", href=re.compile("http")):
			href = link.get("href")
			self.links.append(href)

	def getLinks(self):
		return self.links

	def printLinks(self):
		print ""
		print "Printing links.."
		print self.links
		print ""

	def isWikiPage(self, url):
		wiki = re.compile("wiki")
		found = wiki.search(url)
		print found
		if found:
			print "Url is a wiki page!"
			return True
		else:
			print "Url is not a wiki page!" 
			return False


#this class creates a webcrawler and handles the crawling

#instantiated with starting url (seed)
#crawls until pagesVisited == maxPages
#passes url from path list to Parser 
#Parser returns links scraped from webpage
#crawler then proceeds to next url in path
class Crawler:

	def __init__(self, target_url, max_num_pages):
		self.seed = target_url
		self.path = [self.seed] #first element in path is seed
		self.maxPages = max_num_pages
		self.pagesVisited = 0

	def crawl(self):
		print("Crawling until " + self.maxPages + " reached.")
		while self.pagesVisited < int(self.maxPages):

			print ""
			print("Visiting " + self.path[self.pagesVisited] + "...")

			myParser = Parser(self.path[self.pagesVisited])
			page_scraped = myParser.makeRequest()

			if(page_scraped):
				new_links = myParser.getLinks()
				self.path = self.path + new_links

			self.pagesVisited = self.pagesVisited + 1
			print "Pages visited so far: %d" % (self.pagesVisited)

		#return links in path after crawling is complete
		return self.path

class Results:

	def __init__(self):
		self.query = ""
		self.seed = ""
		self.results = []
		self.filename = ""

	#overload constructor
	def __init__(self, query, seed):
		self.query = query;
		self.seed = seed;
		self.results = []
		self.filename = query + "_results.txt"

	def getResults(self, url_list):
		self.results = url_list

	def printResults(self):

		for item in self.results:
			print item

	def writeResults(self):

		target_file = open(self.filename, "w")

		for item in self.results:
			target_file.write(item + "\n")

		target_file.close()

#this class handles the user query

#insantiated with base url for seed (Wikipedia)
#asks user for query, processes query, generates seed
#initiates crawler if url is valid
#prints results when crawling is finished
class Query:

	def __init__(self):
		self.baseUrl = "https://en.wikipedia.org/wiki/"
		self.raw_query = self.askForQuery()
		self.query = self.processQuery()
		self.seed = self.makeSeed()
		self.maxPages = self.askForMaxPages()
		self.seedValid = self.validateSeed() #boolean value
		self.results = [] #initialize as empty array

	def askForQuery(self):

		user_query = raw_input("Enter your research topic: ")
		return user_query

	def processQuery(self):

		# convert spaces in string to dash
		query = self.raw_query
		query = query.replace(" ", "_")
		return query

	def makeSeed(self):

		return self.baseUrl + self.query

	def getSeed(self):

		if(self.seedValid):
			return self.baseUrl + self.query
		else:
			return "Cannot return invalid url."

	def validateSeed(self):
		print("Validating " + self.seed + " ...")
		# TODO: write code to filter out any .pdf urls
		response = requests.get(self.seed)
		if(response.status_code == requests.codes.ok):
			print "Seed valid!"
			return True
		else:
			print "Seed not valid!"
			return False

	def askForMaxPages(self):
		user_max_pages = raw_input("Enter a limit for the number of pages you want to crawl: ")
		return user_max_pages


	def printResults(self, results):

		print "Results from crawl: "
		for item in results:
			print item

# uncomment code below to run program
#myQuery = Query()
#myCrawler = Crawler(myQuery.seed, myQuery.maxPages) #instantiate Crawler

#print("Starting to crawl " + myQuery.maxPages + " webpages.")
#.results = myCrawler.crawl() # start crawling
#myResults = Results(myQuery.query, myQuery.seed) #instantiate Results
#myResults.getResults(myQuery.results)
#myResults.printResults() # print results to terminal
#myResults.writeResults() # write results to .txt file

