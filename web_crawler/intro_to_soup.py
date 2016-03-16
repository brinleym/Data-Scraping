import re
import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Web_crawler'

source_code = requests.get(url)

plain_text = source_code.text

soup = BeautifulSoup(plain_text, 'html.parser')

print ""
print "Finding links in reference section.."
print ""

#find all links in Wikipedia's reference section
for link in soup.select('.reference-text a'):
	href = link.get('href')
	print href

print ""
print "Finding reference links that begin with http.."
print ""

#find all external reference links on Wikipedia page
for link in soup.select('.reference-text .external'):
	href = link.get('href')
	print href

print ""
print "Finding reference links that begin with http using find_all().."
print ""

links = []
#find all external reference links on Wikipedia page
for link in soup.find_all('a', class_="external", href=re.compile("http")):
	href = link.get('href')
	links.append(href)
	print href

print ""
print "Printing links array..."
print ""

for item in links:
	print item
