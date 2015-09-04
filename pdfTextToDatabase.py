#!/usr/bin/env python
# encoding: utf-8

"""
pdfTextToDatabase.py

1. Get a list of PDF names from the database
2. Open them
3. Extract text contents
4. Write contents back to the database

"""

from hrcemail_common import *
import string
import slate
import sys

def extract(filename):
	try:
		file = open('pdfs/'+filename+'.pdf', 'rb')
	except:
		return None;
	try:
		#this removes non-ASCII characters. Might not be desirable in some circumstances.
		return filter(lambda x: x in string.printable,"\n".join(slate.PDF(file)))
	except:
		return None;
		
docIDs = Document.select(Document.docID)

for docID in docIDs:
	filename = docID.docID
	print "Working on",filename
	output_string = extract(filename)
	insert_query = Document.update(docText = output_string).where(Document.docID == filename)
	insert_query.execute()
