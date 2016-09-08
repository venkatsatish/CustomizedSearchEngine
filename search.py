from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in
from whoosh import index
from whoosh import qparser
from whoosh.qparser import QueryParser
import re,os,codecs
import sys

ix=index.open_dir("database")
with ix.searcher() as searcher:
	queryString = ""
	for index in range(1, len(sys.argv)):
		queryString+=sys.argv[index]+" "
	qparserObject = qparser.MultifieldParser(["id","content"], ix.schema,group=qparser.syntax.OrGroup.factory(0.9))
	query = qparserObject.parse(queryString)
	corrected = searcher.correct_query(query, queryString)
	if corrected.query != query:
		print "Did you mean:" + corrected.string
		print "Showing results for " + corrected.string
		newQuery = qparserObject.parse(corrected.string)
		correctedResults = searcher.search(newQuery)   #these are the results
		for hit in correctedResults:
			print len(correctedResults)
			print hit["id"]
			print hit.highlights("content", top=5)    #not working as expected showing html code sometimes leaving highlights of a file
	else:
		results = searcher.search(query)
		for hit in results:
			print hit["id"]
			print hit.highlights("content", top=5)
