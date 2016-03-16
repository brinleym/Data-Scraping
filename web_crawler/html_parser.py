#very basic html parser
import HTMLParser
import urllib

#array to hold user-friendly webpage content
human_readable_content = [];

class Parser(HTMLParser.HTMLParser):

	#this is a method called to process arbitrary data
	def handle_data(self, data):
		if data != '\n':
			human_readable_content.append(data)


#Create instance of HTML parser
myParser = Parser()

url = 'https://en.wikipedia.org/wiki/Web_crawler'

response = urllib.urlopen(url);

html_goop = response.read()

myParser.feed(html_goop)
myParser.close()

#print parsed content
for item in human_readable_content:
	print item