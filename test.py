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
from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

#Function that removes all the lines with tags style and script and document and head and title and also comments
# def visible(element):
#     if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
#         return False
#     elif re.match('<!--.*-->',element.encode('utf-8')):
#         return False
#     return True

ix=index.open_dir("database")

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search',methods = ['POST', 'GET'])
def search():
	#open only the sample directory
	if request.method == 'POST': 
		queryString = request.form["search"]
		return searcher(queryString)

def searcher(queryString):	
	schema = Schema(id=ID(stored=True),content=TEXT(stored = True))
	with ix.searcher() as searcher:
		qparserObject = qparser.MultifieldParser(["id","content"], ix.schema,group=qparser.syntax.OrGroup.factory(0.9) )
		query = qparserObject.parse(queryString)
		results = searcher.search(query,limit=None)
		corrected = searcher.correct_query(query, queryString)
		if corrected.query != query:
			print "Did you mean:" + corrected.string
			print "Showing results for " + corrected.string
			newQuery = qparserObject.parse(corrected.string)
			correctedResults = searcher.search(newQuery,terms=True)   #these are the results
			print len(correctedResults)
			for hit in correctedResults:
				print hit.highlights("content",top = 5)
				return hit.highlights("content",top = 5)
		else:
			results = searcher.search(query)
			print(len(results))
			for hit in results:
				print hit.highlights("content",top=5)
				return hit.highlights("content",top = 5)

if __name__ == '__main__':
	app.run(debug = True)
