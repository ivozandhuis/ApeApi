#! /usr/bin/env python3

# APE2CSV
# This Python3 script handles a query to the API v1 of Archives Portal Europe
# (see  http://www.archivesportaleurope.net/information-api)
# ... creates searchresult.csv with the result;
# ... creates testresult.csv with a log of the request urls, the response size and -time.
# NB1! This script is originally for testing. Therefor it runs for a maximum of ca. 5 min. 
# NB2! Put your personal APIkey and query-search-terms from line 19 onwards!
# Ivo Zandhuis (http://ivozandhuis.nl) 20160509
# Licence: CC0

import requests
import json
import csv
import time
import sys

# --> Add your personal APIkey and query here!
APIkey = 'myApiKeyXXXX123456789'
query = 'myQuery'

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError:
    return False
  return True

# endpoint
base_url = "https://api.archivesportaleurope.net/services"

# create dict header
header = {}
header['accept'] = 'application/vnd.ape-v1+json; charset=utf8'
header['APIkey'] = APIkey

# create basic dict payload for POST-requests on /search/ead
payload = {}
payload['query'] = query
payload['count'] = 5

# setting up CSV files
searchresult = open('searchresult.csv', 'w')
wr1 = csv.writer(searchresult, quoting=csv.QUOTE_ALL)
wr1.writerow(("index","id","repository","unitId","unitTitle"))
testresult = open('testresult.csv', 'w')
wr2 = csv.writer(testresult, quoting=csv.QUOTE_ALL)
wr2.writerow(("index","url","size (bytes)","time (ms)"))

# requesting and iterating through the results
totalResults = 1 # dummy value to get started...
i = 0 # index, numbering the results
t = 300000 # script runs a maximum of ca. 5 minutes (= 300000 ms)
while ((i < totalResults) and (t > 0)):
	# create request
	payload['startIndex'] = i
	service = '/search/ead'
	url = base_url + service
	print(url) # print on STOUT for user feedback
	# do request
	start = time.time() # start measuring response time
	r = requests.post(url, headers=header, data=json.dumps(payload))
	end = time.time() # end measuring response time
	# write log in testresult.csv
	deltaTime = int((end - start) * 1000)
	size = sys.getsizeof(r.text)
	testResult = ("--", url, size, deltaTime)
	wr2.writerow(testResult) # write testresult to testresult.csv
	t = t - deltaTime
	# handling response
	if is_json(r.text):
		jsonResultlist = json.loads(r.text)
	else:
		print(r.text)
		break
	totalResults = jsonResultlist['totalResults']	
	eadSearchResults = jsonResultlist['eadSearchResults']
	for item in eadSearchResults:
		# create request detailed info
		if item['docType'] == 'Descriptive Unit':
			service = '/content/descriptiveUnit/'
		else:
			service = '/content/'
		request = item['id']
		url = base_url + service + request
		print(url) # print on STOUT for user feedback
		# do request
		start = time.time() # start measuring response time
		r = requests.get(url, headers=header) # do the request
		end = time.time() # end measuring response time
		# write log in testresult.csv
		deltaTime = int((end - start) * 1000)
		size = sys.getsizeof(r.text)
		testResult = (i, url, size, deltaTime)
		wr2.writerow(testResult) # write testresult to testresult.csv
		t = t - deltaTime			
		# handling response
		if is_json(r.text):
			jsonDetails = json.loads(r.text)
		else:
			print(r.text)
			break
		data = (i,) # create list with result
		data = data + (jsonDetails['id'],)
		data = data + (jsonDetails['repository'],)
		data = data + (jsonDetails['unitId'],)
		data = data + (jsonDetails['unitTitle'],)		
		wr1.writerow(data) # write result to searchresult.csv
		i = i + 1

searchresult.close()
testresult.close()

