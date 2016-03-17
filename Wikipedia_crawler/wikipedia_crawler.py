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
			return False # this throws error

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
		
		url = self.url
		title = self.get_header()
		excerpt = self.get_excerpt()

		summary = pageSumm(url, title, excerpt) # instantiate page summary object

		return summary 

	def get_header(self):
		title = self.soup.find("h1") # find first h1 tag and store header text in var
		if title is None:
			title = "No title found."
		else:
			title = title.get_text()

		return title

	def get_excerpt(self):

		excerpt = "No excerpt available."
		all_p_tags = p_list = self.soup.find_all("p") # find all p tags and store in list
		if all_p_tags is not None:
			for item in all_p_tags:
				text = item.get_text()
				if len(text) >= 100:
					excerpt = text
					break

		return excerpt



class Crawler: 

	def __init__(self, seed, path):
		self.seed = seed # wikipedia url
		self.path = path
		self.results = [] # initialize empty list to hold results

	def crawl_rec(self):

		if(len(self.path) == 0): # base case: stop crawling
			self.printResults()
			return "All done"

		# get url 
		url = self.path.pop()

		if(self.validateUrl(url)): # if url is valid..make request for data

			# make request
			newRequest = Request(url)

			# store response (html goop)
			responseText = newRequest.soup

			# parse response
			pageScraper = Scraper(url, responseText) # instantiate scraper
			self.results.append(pageScraper.scrape_page()) # append pageSumm obj returned by scraper to results list

		self.crawl_rec() # keep crawling

	def validateUrl(self, url):
		print("Validating " + url + " ...")
		html = re.compile(".html")
		return html.search(url) # returns boolean: if/if not url points html page

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




myQuery = Query()
myRequest = Request(myQuery.getSeed()) # instantiate request object

responseText = myRequest.soup
myWikiScraper = Scraper(myRequest.url, responseText) # instantiate new scraper object
myWikiScraper.scrape_wiki_references() # tell scraper to parse html stored in soup var

myCrawler = Crawler(myWikiScraper.url, myWikiScraper.wiki_links) # instantiate new crawler object, giving it link path scraped from Wikipedia references
myCrawler.crawl_rec() # start crawling


