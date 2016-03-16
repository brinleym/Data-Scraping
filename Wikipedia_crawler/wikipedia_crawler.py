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
			print "page okay. parsing html..."
		except ConnectionError as error:
			print error
			print "Page not found. Returning false.."
			return False

		return response.text # return plain text 

	def parseHtml(self, text):

		html_soup = BeautifulSoup(text, "html.parser")
		return html_soup


class Scraper: 

	def __init__(self, target_url):
		self.url = target_url
		self.wiki_links = [] #this will be crawler's path

	def scrape_wiki_reference(self, soup):
		print "Scraping Wikipedia reference links.."
		for link in soup.find_all("a", class_="external",
								   href=re.compile("http")):
			href = link.get("href")
			self.wiki_links.append(href)

	def scrape_page(self, soup):
		print "Getting links from non-Wiki.."
		for link in soup.find_all("a", href=re.compile("http")):
			href = link.get("href")
			self.links.append(href)

myQuery = Query()
myRequest = Request(myQuery.getSeed()) # instantiate request object


