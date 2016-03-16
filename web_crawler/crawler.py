#my first web crawler
import HTMLParser
import urllib
import requests

human_readable_content = [];

class Parser(HTMLParser.HTMLParser):

	#this is a method handles the start tag for links
	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for (key, value) in attrs:
				if key == 'href':
					new_url = urllib.parse.urljoin(self.baseUrl, value)
					self.links = self.links + new_url

	def getLinks(self, url):

		print "getting links.."
		#container for webpage links
		self.links = []
		self.baseUrl = url
		handle = urllib.urlopen(url)
		html_gunk = handle.read()
		print html_gunk

		response = requests.get(url)
		print response.headers['Content-Type']
		
		if response.get_header('Content-Type') == 'text/html':
			html_goop = response.read()
			print html_goop
			html_string = html_goop.decode('utf-8')
			self.feed(html_goop)
			return html_string, self.links
		else:
			return '', []

def crawler(url, query, maxPages):
	pages_to_visit = [url]
	num_visited = 0
	foundQuery = False
	while num_visited < maxPages:
		url = pages_to_visit[num_visited]
		try: #bug in this block of code
			print "%d : Visting %s" % (num_visited, url)
			myParser = Parser() #create new instance of Parser
			data, links = myParser.getLinks(url)
			if data.find(query) > -1:
				foundQuery = True
			pages_to_visit = pages_to_visit + links #concat lists
			print "success!"
		except:
			print "failed!"
		num_visited = num_visited + 1
	if foundQuery:
		print "Your query, %s, was found at %s" % (query, url)
	else:
		print "Word never found."

crawler('https://en.wikipedia.org/wiki/Web_crawler', 'web', 10)


#Create instance of HTML parser
#myParser = Parser()

#url = 'https://en.wikipedia.org/wiki/Web_crawler'

#response = urllib.urlopen(url);

#html_goop = response.read()

#myParser.feed(html_goop)
#myParser.close()

#or item in human_readable_content:
	#print item