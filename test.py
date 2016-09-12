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
ix=index.open_dir("final_index")

@app.route('/')
def index():
	return render_template('search.html')


@app.route('/search',methods = ['POST', 'GET'])
def search():
	#open only the sample directory
	if request.method == 'POST': 
		queryString = request.json['query']
		p = request.json['score']
		return searcher(queryString,p)

def searcher(queryString,p):	
	ls = []
	schema = Schema(id=ID(stored=True),img=TEXT(stored=True),title=TEXT(stored=True),h1=TEXT(analyzer=StemmingAnalyzer(),stored=True),content=TEXT(analyzer=StemmingAnalyzer(), stored = True))
	if(p == "1"):
		print "TF_IDF"
		with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
			qparserObject = qparser.MultifieldParser(["id","h1","title","content"],ix.schema)
			query = qparserObject.parse(queryString)
			results = searcher.search(query,limit=10)
			corrected = searcher.correct_query(query, queryString)
			if corrected.query != query:
				print "Did you mean:" + corrected.string
				print "Showing results for " + corrected.string
				newQuery = qparserObject.parse(corrected.string)
				correctedResults = searcher.search(newQuery,terms=True)   
				l = len(correctedResults)
				if(len(correctedResults) != 0):
					for hit in correctedResults:
						a = {}
						print hit["title"]
						a["title"] = hit["title"]
						a["imagetag"] = hit["img"]
						a["file"] = "../final_database/"+hit["id"]+".html"
						a["data"] = hit.highlights("content",top = 5)
						ls.append(a)
					print "hello"
					return render_template('result.html',entries=ls,num=l,query=queryString,sim=0,correct = corrected.string)	
				else:
					return render_template('result.html',correct=queryString,num=0)
			else:
				results = searcher.search(query)
				l = len(results)
				if(len(results) != 0):
					for hit in results:
						a={}
						a["title"] = hit["title"]
						a["imagetag"] = hit["img"]
						a["file"] = "../final_database/"+hit["id"]+".html"
						a["data"] = hit.highlights("content",top = 5)
						ls.append(a)
					return render_template('result.html',entries=ls,num=l,query=queryString,sim=2,correct = corrected.string)	
				else:
					return render_template('result.html',correct=queryString,num=0)
	else:
		with ix.searcher() as searcher:
			qparserObject = qparser.MultifieldParser(["id","h1","content"],ix.schema)
			query = qparserObject.parse(queryString)
			results = searcher.search(query,limit=None)
			corrected = searcher.correct_query(query, queryString)
			if corrected.query != query:
				print "Did you mean:" + corrected.string
				print "Showing results for " + corrected.string
				newQuery = qparserObject.parse(corrected.string)
				correctedResults = searcher.search(newQuery,terms=True)
				l = len(correctedResults)
				if(len(correctedResults) != 0):
					for hit in correctedResults:
						print hit["title"]
						a = {}
						a["title"] = hit["title"]
						a["imagetag"] = hit["img"]
						a["file"] = "../final_database/"+hit["id"]+".html"
						a["data"] = hit.highlights("content",top = 5)
						ls.append(a)
					print "hello"
					return render_template('result.html',entries=ls,num=l,query=queryString,sim=0,correct = corrected.string)
				else:
					return render_template('result.html',correct=queryString,num=0)
			else:
				results = searcher.search(query)
				l = len(results)
				if(len(results) != 0):
					for hit in results:
						a = {}
						a["title"] = hit["title"]
						a["imagetag"] = hit["img"]
						a["file"] = "../final_database/"+hit["id"]+".html"
						a["data"] = hit.highlights("content",top = 5)
						ls.append(a)
					return render_template('result.html',entries=ls,num=l,query=queryString,sim=3,correct = corrected.string)	
				else:
					return render_template('result.html',correct=queryString,num=0)
if __name__ == '__main__':
	app.run(debug = True,port=8081)
