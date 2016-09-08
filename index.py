# added features multifield and or grouping, Variations
# to be added FLASK, Autocomplete, SpellChecker, Header tags, lowercase*


from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in
from whoosh import index
from bs4 import BeautifulSoup
from whoosh import qparser
from whoosh.qparser import QueryParser
import re,os,codecs,sys

#Function that removes all the lines with tags style and script and document and head and title and also comments
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->',element.encode('utf-8')):
        return False
    return True

schema = Schema(id=ID(stored=True),content=TEXT(stored = True))
dir = os.listdir('sample')
ix = create_in("database", schema)
for l in dir:
	print l
	p = "sample/"+l
	html = codecs.open( p , "r", "utf-8" ).read()
	soup = BeautifulSoup(html, 'html.parser')
	texts = soup.findAll(text=True)
	visible_texts = filter(visible, texts)
	s = u''
	for elem in visible_texts:
		if( elem != u''):
			s += elem.strip(" \n\t\r")+" "
	writer = ix.writer()
	writer.add_document(id=l.strip(".html").decode('utf-8'),content = s)
	writer.commit()
