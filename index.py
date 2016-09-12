
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in
from whoosh import index
from bs4 import BeautifulSoup
from whoosh import qparser
from whoosh.qparser import QueryParser
import re,os,codecs,sys,progressbar

#Function that removes all the lines with tags style and script and document and head and title and also comments
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->',element.encode('utf-8')):
        return False
    return True

schema = Schema(id=ID(stored=True),img=TEXT(stored=True),title=TEXT(stored=True),h1=TEXT(analyzer=StemmingAnalyzer()),content=TEXT(analyzer=StemmingAnalyzer(), stored = True))
dir = os.listdir('final_database')
ix = create_in("final_index", schema)
with progressbar.ProgressBar(maxval=21890, widgets=[' [', progressbar.Timer(), '][', progressbar.ETA(), '][', progressbar.Percentage(), ']', progressbar.Bar('=', '[', '] '), progressbar.Counter()]) as bar:
	for i, l in enumerate(dir):
		bar.update(i+1)
		p = "final_database/"+l
		html = codecs.open( p , "r", "utf-8" ).read()
		soup = BeautifulSoup(html, 'html.parser')
		tit = u''
		tit += soup.title.string
		imgs = soup.find('h1').find_all_next('img')[0]
		im = u'https:'
		im += imgs["src"]
		texts = soup.findAll(text=True)
		visible_texts = filter(visible, texts)
		div = soup.find("div", {"id": "content"})
		headers = div.find_all(['h1', 'h2', 'h3'])
		p = u''
		for header in headers:
			if header.get_text().endswith("[edit]"):
				p += header.get_text()[:-len("[edit]")] + " "
		s = u''
		for elem in visible_texts:
			if( elem != u''):
				s += elem.strip(" \n\t\r")+" "
		writer = ix.writer()
		writer.add_document(id=l.strip(".html").decode('utf-8'),img=im,title=tit,h1=p,content = s)
		writer.commit()
