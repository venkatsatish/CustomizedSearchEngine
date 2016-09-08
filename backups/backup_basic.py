# added features multifield and or grouping, Variations, SpellChecker
# to be added FLASK, Autocomplete, Header tags, lowercase*


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

#open only the sample directory 
ix=index.open_dir("../database") 
schema = Schema(id=ID(stored=True),content=TEXT(stored = True))
with ix.searcher() as searcher:
	queryString = ""
	for index in range(1, len(sys.argv)):
		queryString+=sys.argv[index]+" "
	qparserObject = qparser.MultifieldParser(["id","content"], ix.schema,group=qparser.syntax.OrGroup.factory(0.9))
	query = qparserObject.parse(queryString)
	results = searcher.search(query)
	corrected = searcher.correct_query(query, queryString)
	if corrected.query != query:
		print "Did you mean:" + corrected.string
		print "Showing results for " + corrected.string
		newQuery = qparserObject.parse(corrected.string)
		correctedResults = searcher.search(newQuery,terms=True)   #these are the results
		print len(correctedResults)
		for hit in correctedResults:
			print(hit["id"])
			print( hit.highlights("content",top = 5)+"\n")    #not working as expected showing html code sometimes leaving highlights of a file
	else:
		results = searcher.search(query)
		print(len(results))
		for hit in results:
			print(hit["id"])
			print(hit.highlights("content",top=5)+"\n")


# dir = os.listdir('sample')
# ix = create_in("database", schema)
# for l in dir:
# 	print l
# 	p = "sample/"+l
# 	html = codecs.open( p , "r", "utf-8" ).read()
# 	soup = BeautifulSoup(html, 'html.parser')
# 	texts = soup.findAll(text=True)
# 	visible_texts = filter(visible, texts)
# 	s = u''
# 	for elem in visible_texts:
# 		if( elem != u''):
# 			s += elem.strip(" \n\t\r")+" "
# 	writer = ix.writer()
# 	writer.add_document(id=l.decode('utf-8'),content = s)
# 	writer.commit()
