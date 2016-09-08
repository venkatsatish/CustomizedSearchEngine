from bs4 import BeautifulSoup

page = "sample/100862.html"
html = open(page).read()
soup = BeautifulSoup(html, 'html.parser')
for script in soup(["script", "style"]):
	script.extract()
text = soup.get_text()
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = ' '.join(chunk for chunk in chunks if chunk) # clean text along with link test
print text