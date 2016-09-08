from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in
from whoosh import index
from bs4 import BeautifulSoup
from whoosh.qparser import QueryParser
import re,os,codecs
import progressbar

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->',element.encode('utf-8')):
        return False
    return True

dir = os.listdir('dataset')
schema = Schema(content=TEXT(stored = True))
ix = create_in("database", schema)

with progressbar.ProgressBar(maxval=21890, widgets=[' [', progressbar.Timer(), '][', progressbar.ETA(), '][', progressbar.Percentage(), ']', progressbar.Bar('=', '[', '] '), progressbar.Counter()]) as bar:

	for i, l in enumerate(dir):
		bar.update(i+1)
		# print l
		p = "dataset/"+l
		html = codecs.open( p , "r", "utf-8" ).read()
		# import pdb; pdb.set_trace()
		soup = BeautifulSoup(html, 'html.parser')
		texts = soup.findAll(text=True)
		visible_texts = filter(visible, texts)
		s = u''
		for elem in visible_texts:
			if( elem != u''):
				s += elem.strip(" \n\t\r")+" "
		writer = ix.writer()
		writer.add_document(content = s)
		writer.commit()

	
with ix.searcher() as searcher:
	query = QueryParser("content", ix.schema).parse("INSAT")
	results = searcher.search(query)
	print results[0]
