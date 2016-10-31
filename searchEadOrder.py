#! /usr/bin/env python3


serviceToTest = '/search/ead'
sortoptions = ["date", "findingAidNo", "title", "referenceCode"]

# Python3 script to test the services of the API of Archives Portal Europe
# see http://www.archivesportaleurope.net/information-api
# see http://www.github.com/ivozandhuis/APEAPI

import requests
import json
import csv
import time
import datetime
import sys
import math


import APElib

# --> Endpoint and key are set by APElib.py, otherwise overwrite them here:
base_url = APElib.setBaseurl()
APIkey   = APElib.setAPIkey()
accept   = APElib.setAccept()

# --> Change your personal query here:
query = 'louis'

# create dict header
header = {}
header['accept'] = accept
header['APIkey'] = APIkey

sortRequest = {}

# create basic dict payload for POST-requests on /search/ead
payload = {}
payload["query"] = query
payload["count"] = 5


# list of all potential responsevariables in the resultlist
csvHeader = ["id","fondsUnitTitle","fondsUnitId","repository","country","language","langMaterial","unitDate","repositoryCode","hasDigitalObject","docType", "docTypeId","level","indexDate","unitId","unitTitle","unitTitleWithHighlighting","scopeContent","scopeContentWithHighlighting"]

# setting up CSV files
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

filename1 = 'searchEadOrderResult' + st + '.csv'
filename2 = 'searchEadOrderPerformance' + st + '.csv'

searchresult = open(filename1, 'w')
wr1 = csv.writer(searchresult, quoting=csv.QUOTE_ALL)
wr1.writerow(["index"] + csvHeader)
testresult = open(filename2, 'w')
wr2 = csv.writer(testresult, quoting=csv.QUOTE_ALL)
wr2.writerow(("index","url","size (bytes)","time (ms)"))

for n in range(8):
	# requesting and iterating through the results
	totalResults = 1 # dummy value to get started...
	i = 0 # index, numbering the results
	t = 30000 # script runs a maximum of ca. 5 minutes (= 300000 ms)
	while ((i < totalResults) and (t > 0)):
		# create request
		if n % 2 == 0: 
			sortRequest["sortType"] = "asc"
		else:
			sortRequest["sortType"] = "desc"			
		sortRequest["fields"] = [sortoptions[math.floor(n/2)]]
		payload["sortRequest"] = sortRequest
		payload['startIndex'] = i
		service = serviceToTest
		url = base_url + service
		print("*", end="", flush=True)
		# do request
		start = time.time() # start measuring response time
		r = requests.post(url, headers=header, data=json.dumps(payload))
		end = time.time() # end measuring response time
		# write log in *Performance.csv
		deltaTime = int((end - start) * 1000)
		size = sys.getsizeof(r.text)
		testResult = ("--", url, size, deltaTime, payload)
		wr2.writerow(testResult) # write testresult to *Performance.csv
		t = t - deltaTime
		# handling response
		if APElib.is_json(r.text):
			jsonResultlist = json.loads(r.text)
		else:
			print(r.text)
			break
		totalResults = jsonResultlist['totalResults']	
		eadSearchResults = jsonResultlist['eadSearchResults']
		for item in eadSearchResults:
			data = (i,) # create list with result
			keyList = item.keys()
			for head in csvHeader:
				if head in keyList:
					data = data + (item[head],)
				else:
					data = data + ('NOT AVAILABLE',)
			wr1.writerow(data) # write result to *Result.csv
			i = i + 1

print("\n")
searchresult.close()
testresult.close()

