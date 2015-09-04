#!/usr/bin/env python
# encoding: utf-8

"""
generatePDFList.py

1. Get list of links from database
2. Write out file for wget to use
"""

from hrcemail_common import *

pdf_base = "https://foia.state.gov/searchapp/"

with open('pdflist.txt', 'w') as list_file:
	for doc in Document.select():
		list_file.write(pdf_base+doc.pdfLink+"\n")
