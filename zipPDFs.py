#!/usr/bin/env python
# encoding: utf-8

"""
zipPDFs.py

1. Get a list of files from the database
2. For each distinct documentClass, create a zip file
3. Write the PDFs into each zip file from pdfs/

"""

from hrcemail_common import *
import zipfile
import os

docClasses = (Document.select(fn.Distinct(Document.documentClass).alias("docClass")))

for docClass in docClasses:
	print "working on ",docClass.docClass
	if not os.path.isfile("zips/"+docClass.docClass+".zip"):
		with zipfile.ZipFile("zips/"+docClass.docClass+".zip", "w") as zf:
			docIDs = (Document.select(Document.docID).where(Document.documentClass == docClass.docClass))
			for docID in docIDs:
				if os.path.isfile("pdfs/"+docID.docID+".pdf"):
					zf.write("pdfs/"+docID.docID+".pdf", docID.docID+".pdf")
