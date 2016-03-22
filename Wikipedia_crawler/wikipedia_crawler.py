import re # regex library
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from modules import Query
from modules import Results

class Request:

	def __init__(self, target_url):
		self.url = target_url
		self.plain_text = self.makeRequest(self.url)
		self.soup = self.parseHtml(self.plain_text)
		
	def makeRequest(self, url):
		try:
			response = requests.get(url) # make GET request
		except ConnectionError as error:
			print error
			print "Page not found. Bypassing page.."
			return None

		return response.text # return plain text 

	def parseHtml(self, text):

		# corner case: request failed, no response text to parse
		if self.plain_text is None: 
			return None

		html_soup = BeautifulSoup(text, "html.parser")
		return html_soup


class Scraper: 

	def __init__(self, target_url, html):
		self.url = target_url
		self.soup = html
		self.wiki_links = [] # this will be crawler's path

	def scrape_wiki_references(self):
		print "Scraping Wikipedia reference links.."
		for link in self.soup.find_all("a", class_="external",
								   href=re.compile("http")):
			href = link.get("href")
			self.wiki_links.append(href)

	def scrape_page(self):
		print "Scraping non-Wiki page.."
		
		url = self.url
		title = self.get_header()
		excerpt = self.get_excerpt()

		# instantiate pageSumm
		summary = pageSumm(url, title, excerpt) 

		return summary 

	def get_header(self):

		# find first h1 tag
		title = self.soup.find("h1") 
		if title is None:
			title = "No title found."
		else:
			title = title.get_text()

		return title

	def get_excerpt(self):

		excerpt = "No excerpt available."

		# find all p tags and store in list
		all_p_tags = p_list = self.soup.find_all("p") 
		if all_p_tags is not None:
			for item in all_p_tags:
				text = item.get_text()
				length = len(text)
				if length >= 100 and length < 500:
					excerpt = text
					break

		return excerpt



class Crawler: 

	def __init__(self, seed, path):
		# wikipedia page matching user query
		self.seed = seed 
		# list of wikipedia reference links to crawl
		self.path = path 
		# list of pageSumm's
		self.results = [] 

	def crawl_rec(self):

		# base case: if path list is empty, stop crawling
		if(len(self.path) == 0): 
			self.printResults()
			return True # done crawling

		# get url 
		url = self.path.pop()

 		# if url is valid, make request for data
		if(self.validateUrl(url)):

			# make request
			newRequest = Request(url)

			# store response (Beautiful soup object)
			responseText = newRequest.soup

			# if request succeeded, parse response
			if(responseText is not None): 

				# instantiate scraper
				pageScraper = Scraper(url, responseText) 

				# append pageSumm obj returned by scraper to results list
				self.results.append(pageScraper.scrape_page())

		# keep crawling
		self.crawl_rec() 

	# returns boolean: if/if not url points to .html page
	def validateUrl(self, url):
		print("Validating " + url + " ...")
		html = re.compile(".html")
		return html.search(url) 

	def printResults(self):

		for item in self.results:
			print("Url: " + item.getUrl())
			print("Title: " + item.getTitle())
			print("Excerpt: " + item.getExcerpt())


class pageSumm:

	def __init__(self, url, title, exerpt):
		self.url = url
		self.title = title
		self.exerpt = exerpt

	def getUrl(self):

		return self.url

	def getTitle(self):

		return self.title

	def getExcerpt(self):

		return self.exerpt



# get user query
myQuery = Query()

# getSeed() returns Wikipedia url matching user query
# if Wikipedia page exists, returns url
# if page does not exist, returns None
wiki_url = myQuery.getSeed()

if wiki_url is not None:

	# make request with Request object
	myRequest = Request(wiki_url) 

	# get response
	responseText = myRequest.soup 

	# if request was success 
	if responseText is not None:
		
		# instantiate new Scraper object to scrape wikipedia page
		myWikiScraper = Scraper(myRequest.url, responseText) 
		
		# ask scraper to scrape external links in wikipedia page
		myWikiScraper.scrape_wiki_references()

		# if scraper has found at least one external link on wikipedia page
		if len(myWikiScraper.wiki_links) > 0:

			# instantiate new Crawler object 
			# crawler's seed is wikipedia page
			# crawler's path is all external links scraped from wikipedia page
			myCrawler = Crawler(myWikiScraper.url, myWikiScraper.wiki_links)

			# start crawling
			myCrawler.crawl_rec() 


# crawling is over 

# make new Results object
myResults = Results(myQuery.query, myQuery.seed)

# get results from crawler
myResults.getResults(myCrawler.results)

# write results to .txt file
myResults.writeResults() # throws error, cannot write objects to text file


