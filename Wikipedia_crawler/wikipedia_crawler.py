import re # regex library
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from modules import Query

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
			print "Page not found. Returning false.."
			return False

		return response.text # return plain text 

	def parseHtml(self, text):

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
		title = self.soup.find("h1") # find first h1 tag
		url = self.url
		content = ""

		summary = pageSumm(url, title, content) # instantiate page summary object

		print summary.url
		print summary.title
		print summary.content

		return summary 


class Crawler: 

	def __init__(self, seed, path):
		self.seed = seed # wikipedia url
		self.path = path
		self.results = [] # initialize empty list to hold results

	def crawl_rec(self):

		if len(self.path) == 0: # base case: stop crawling
			self.printResults()
			return "All done"

		# get url 
		url = self.path.pop()

		# make request
		newRequest = Request(url)

		# store response (html goop)
		responseText = newRequest.soup

		# parse response
		pageScraper = Scraper(url, responseText) # instantiate scraper
		self.results.append(pageScraper.scrape_page()) # append pageSumm obj returned by scraper to results list

		self.crawl_rec() # keep crawling

	def printResults():

		for item in self.results:
			print item

class pageSumm:

	def __init__(self, url, title, content):
		self.url = url
		self.title = title
		self.content = content




myQuery = Query()
myRequest = Request(myQuery.getSeed()) # instantiate request object

responseText = myRequest.soup
myWikiScraper = Scraper(myRequest.url, responseText) # instantiate new scraper object
myWikiScraper.scrape_wiki_references() # tell scraper to parse html stored in soup var

myCrawler = Crawler(myWikiScraper.url, myWikiScraper.wiki_links) # instantiate new crawler object, giving it link path scraped from Wikipedia references
myCrawler.crawl_rec() # start crawling


