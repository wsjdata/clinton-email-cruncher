#!/usr/bin/env python
# encoding: utf-8

"""
downloadMetadata.py

1. Page through the Clinton_Email collection on state.foia.gov
2. Write rows to sqlite db, ON DUPLICATE KEY UPDATE VALUES

"""

from datetime import datetime
import requests
import requests_cache
import certifi
import re
import json
import sys
from hrcemail_common import *

requests_cache.install_cache("HRCEMAIL_metadata_cache",expire_after=300)

query_base = "https://foia.state.gov/searchapp/Search/SubmitSimpleQuery"

def getAPIPage(start=0,limit=1000,page=1):
	params = {"searchText": "*",
	"beginDate": "false",
	"endDate": "false",
	"collectionMatch": "Clinton_Email",
	"postedBeginDate": "false",
	"postedEndDate": "false",
	"caseNumber": "false",
	"page":page,
	"start": start,
	"limit": limit}
	
	#SSL certificate not verified by certifi module for some reason	
	request = requests.get(query_base,params=params)
		
	return_json = request.text
	#date objects not valid json, extract timestamp
	return_json = re.sub(r'new Date\(([0-9]{1,})\)',r'\1',return_json)
	#negitive dates are invalid, and can sometimes be shown as newDate()
	return_json = re.sub(r'new ?Date\((-[0-9]{1,})\)',r'null',return_json)
	return json.loads(return_json)

def compileResultsList(results_list=[],start=0, limit=1000):
	metadata_response = getAPIPage(start=start,limit=limit)
	results_list.extend(metadata_response["Results"])
	if len(results_list) < metadata_response["totalHits"]:
		start += limit
		compileResultsList(results_list=results_list,start=start,limit=limit)
	elif len(results_list) > metadata_response["totalHits"]:
		sys.exit("error, results count mismatch")
	return results_list
	
def formatTimestamp(timestamp):
	try:
		return datetime.fromtimestamp(timestamp/1000).strftime("%Y-%m-%d")
	except TypeError:
		return None

results_list = compileResultsList()

print "got",len(results_list),"total document rows"
print "writing rows to sqlite database ..."

with db.transaction():
	for result in results_list:
		result["messageFrom"] = result["from"]
		del result["from"]
		result["docDate"] = formatTimestamp(result["docDate"])
		result["postedDate"] = formatTimestamp(result["postedDate"])
		result["docID"] = result["pdfLink"][-13:][0:9]
		result["attachmentOf"] = None
		try:
			Document.create(**result)
		except IntegrityError:
			#only insert new rows, don't update existing rows
			pass

