# added features multifield and or grouping, Variations, SpellChecker
# to be added FLASK, Autocomplete, Header tags, lowercase*


from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in
from whoosh import index
from whoosh import scoring
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

ix=index.open_dir("sippy")

@app.route('/')
def index():
	return render_template('rough.html')

@app.route('/search',methods = ['POST', 'GET'])
def search():
	#open only the sample directory
	if request.method == 'POST': 
		queryString = request.form["search"]
		return searcher(queryString)

def searcher(queryString):	
	schema = Schema(id=ID(stored=True),content=TEXT(analyzer=StemmingAnalyzer(), stored = True))
	with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
		qparserObject = qparser.MultifieldParser(["id","content"],ix.schema)
		query = qparserObject.parse(queryString)
		results = searcher.search(query,limit=None)
		corrected = searcher.correct_query(query, queryString)
		if corrected.query != query:
			print "Did you mean:" + corrected.string
			print "Showing results for " + corrected.string
			newQuery = qparserObject.parse(corrected.string)
			correctedResults = searcher.search(newQuery,terms=True)   #these are the results
			print len(correctedResults)
			if(len(correctedResults) != 0):
				for hit in correctedResults:
					print(hit["id"])
					return hit.highlights("content",top = 5)
					#print hit.highlights("content",top = 5)+"\n"
				#return hit.highlights("content",top = 5)
			else:
				return "<html>No results</html>"
		else:
			results = searcher.search(query)
			print(len(results))
			if(len(results) != 0):
				for hit in results:
					print(hit["id"])
					return hit.highlights("content",top = 5)
				
			else:
				return "<html>No results</html>"

if __name__ == '__main__':
	app.run(debug = True,host = "0.0.0.0")
