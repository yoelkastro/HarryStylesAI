import os
import argparse
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import socket
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

currentReadText = '' 

class ParagraphParser(HTMLParser):
	willRead = False
	def handle_starttag(self, tag, attrs):
		if(tag == 'p' and not attrs[0][0] == 'class'):
			self.willRead = True
		else:
			self.willRead = False

	def handle_data(self, data):
		global currentReadText
		if(self.willRead):
			currentReadText += data + '\n'

def getHtml(url):
	tries = 10
	req = urllib.request.Request(url)
	req.add_header('User-agent', 'Mozilla/5.0 (Linux x86_64)')
	    # Add DoNotTrack header, do the right thing even if nobody cares
	req.add_header('DNT', '1')
	while tries > 0:
	    try:
	        request = urllib.request.urlopen(req)
	        tries = 0
	    except socket.timeout:
	        tries -= 1
	    except urllib.error.URLError as e:
	        print("URL Error " + str(e.code) + ": " + e.reason)
	        print("Aborting...")
	        exit()
	    except urllib.error.HTTPError as e:
	        print("HTTP Error " + str(e.code) + ": " + e.reason)
	        print("Aborting...")
	        exit()

	soup = BeautifulSoup(request.read(), "lxml")
	return str(soup)

def parseParagraph(soup):
	pp = ParagraphParser()
	pp.feed(soup)

def readStory(url):
	global currentReadText
	page = 1
	parseParagraph(getHtml(url + '/page/' + str(page)))
	while(not currentReadText == '\n'):
		writeParagraphToFile(currentReadText)
		currentReadText = '\n'
		page += 1
		parseParagraph(getHtml(url + '/page/' + str(page)))

def writeParagraphToFile(text):
	file = open('/Users/yoelkastro/Desktop/writeAI/data.txt', 'a')
	file.write(text)
	file.close

with open('/Users/yoelkastro/Desktop/writeAI/links.txt', 'r') as f:
	content = f.read().splitlines()

for l in content:
	print(l)
	readStory(l)
