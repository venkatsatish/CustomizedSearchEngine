
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

schema = Schema(id=ID(stored=True),content=TEXT(analyzer=StemmingAnalyzer(), stored = True))
dir = os.listdir('dataset')
ix = create_in("sippy1", schema)
with progressbar.ProgressBar(maxval=21890, widgets=[' [', progressbar.Timer(), '][', progressbar.ETA(), '][', progressbar.Percentage(), ']', progressbar.Bar('=', '[', '] '), progressbar.Counter()]) as bar:
	for i, l in enumerate(dir):
		bar.update(i+1)
		p = "dataset/"+l
		html = codecs.open( p , "r", "utf-8" ).read()
		soup = BeautifulSoup(html, 'html.parser')
		texts = soup.findAll(text=True)
		visible_texts = filter(visible, texts)
		for div in soup.findAll('div', attrs={'class': 'content'}):
			print ''.join([x for x in div.h1.contents if isinstance(x, bs4.element.NavigableString)])
		s = u''
		for elem in visible_texts:
			if( elem != u''):
				s += elem.strip(" \n\t\r")+" "
		writer = ix.writer()
		writer.add_document(id=l.strip(".html").decode('utf-8'),content = s)
		writer.commit()
