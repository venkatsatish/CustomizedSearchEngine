from bs4 import BeautifulSoup
import os,codecs
dir = os.listdir('sample')
for file in dir:
	html = codecs.open( "sample/"+file , "r", "utf-8" ).read()
	soup = BeautifulSoup(html, 'html.parser')
	div = soup.find("div", {"id": "content"})
	headers = div.find_all(['h1', 'h2', 'h3'])
	for header in headers:
		if header.get_text().endswith("[edit]"):
			print header.get_text()[:-len("[edit]")]