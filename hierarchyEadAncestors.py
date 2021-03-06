#! /usr/bin/env python3

serviceToTest = '/hierarchy/ead/{id}/ancestors'

# Python3 script to test the services of the API of Archives Portal Europe
# see http://www.archivesportaleurope.net/information-api
# see http://www.github.com/ivozandhuis/APEAPI

import requests
import json
import csv
import time
import datetime
import sys

import APElib

# --> Endpoint and key are set by APElib.py, otherwise overwrite them here:
base_url = APElib.setBaseurl()
APIkey = APElib.setAPIkey()
accept = APElib.setAccept()

# --> Change your personal query here:
query = 'nepal'

# create dict header
header = {}
header['accept'] = accept
header['APIkey'] = APIkey

# list of all potential responsevariables in the resultlist
csvHeader = ["id","fondsUnitTitle","fondsUnitId","repository","country","language","langMaterial","unitDate","repositoryCode","hasDigitalObject","docType", "docTypeId","level","indexDate","unitId","unitTitle","scopeContent","siblingPosition","ancestorLevel"]

# setting up CSV files
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

filename1 = 'hierarchyEadAncestorsResult' + st + '.csv'
filename2 = 'hierarchyEadAncestorsPerformance' + st + '.csv'

searchresult = open(filename1, 'w')
wr1 = csv.writer(searchresult, quoting=csv.QUOTE_ALL)
wr1.writerow(["index"] + csvHeader)
testresult = open(filename2, 'w')
wr2 = csv.writer(testresult, quoting=csv.QUOTE_ALL)
wr2.writerow(("index","url","size (bytes)","time (ms)"))

# create basic dict payload for POST-requests
payload = {}
payload['query'] = query
payload['count'] = 25

# create and do request
payload['startIndex'] = 0
service = "/search/ead/"
url = base_url + service
print("*", end="\n", flush=True)
r = requests.post(url, headers=header, data=json.dumps(payload))

# handling response
jsonResultlist = json.loads(r.text)
totalResults = jsonResultlist['totalResults']	
eadSearchResults = jsonResultlist['eadSearchResults']
duList = ()
for item in eadSearchResults:
	duList = duList + (item["id"],)

# create basic dict payload for POST-requests
payload = {}
payload['count'] = 5

t = 300000 # script runs a maximum of ca. 5 minutes (= 300000 ms)
for thing in duList:
	totalResults = 1 # dummy value to get started...
	i = 0 # index, numbering the results
	while ((i < totalResults) and (t > 0)):
		# create request
		payload['startIndex'] = i
		service = '/hierarchy/ead/' + thing + '/ancestors'
		url = base_url + service
		print("*", end="", flush=True)
		# do request
		start = time.time() # start measuring response time
		r = requests.post(url, headers=header, data=json.dumps(payload))
		end = time.time() # end measuring response time
		# write log in *Performance.csv
		deltaTime = int((end - start) * 1000)
		size = sys.getsizeof(r.text)
		testResult = ("--", url, size, deltaTime)
		wr2.writerow(testResult) # write testresult to *Performance.csv
		t = t - deltaTime
		# handling response
		if APElib.is_json(r.text):
			jsonResultlist = json.loads(r.text)
		else:
			print(r.text)
			break
		totalResults = jsonResultlist['totalResults']	
		eadSearchResults = jsonResultlist['results']
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
print()
searchresult.close()
testresult.close()

