#! /usr/bin/env python3

serviceToTest = '/content/eac-cpf/'

# Python3 script to test the services of the API v1 of Archives Portal Europe
# see http://www.archivesportaleurope.net/information-api
# see http://www.github.com/ivozandhuis/APEAPI

import requests
import json
import csv
import time
import datetime
import sys

import APElib

# --> Endpoint and key are set by config.py, otherwise overwrite them here:
base_url = APElib.setBaseurl()
APIkey   = APElib.setAPIkey()
accept   = APElib.setAccept()

# --> Change your personal query here:
query = 'louis'

# create dict header
header = {}
header['accept'] = accept
header['APIkey'] = APIkey

# create basic dict payload for POST-requests on /search/ead
payload = {}
payload['query'] = query
payload['count'] = 5

# setting up CSV files
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

filename1 = 'contentEac-cpfResult' + st + '.csv'
filename2 = 'contentEac-cpfPerformance' + st + '.csv'

searchresult = open(filename1, 'w')
wr1 = csv.writer(searchresult, quoting=csv.QUOTE_ALL)
wr1.writerow(("index","recordId","nameEntry"))
testresult = open(filename2, 'w')
wr2 = csv.writer(testresult, quoting=csv.QUOTE_ALL)
wr2.writerow(("index","url","size (bytes)","time (ms)"))

# requesting and iterating through the results
totalResults = 1 # dummy value to get started...
i = 0 # index, numbering the results
t = 300000 # script runs a maximum of ca. 5 minutes (= 300000 ms)
while ((i < totalResults) and (t > 0)):
	# create request
	payload['startIndex'] = i
	service = '/search/eac-cpf'
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
	eacSearchResults = jsonResultlist['eacSearchResults']
	for item in eacSearchResults:
		# create request detailed info
		service = serviceToTest
		request = item['id']
		url = base_url + service + request
		print("*", end="", flush=True)
		# do request
		start = time.time() # start measuring response time
		r = requests.get(url, headers=header) # do the request
		end = time.time() # end measuring response time
		# write log in *Performance.csv
		deltaTime = int((end - start) * 1000)
		size = sys.getsizeof(r.text)
		testResult = (i, url, size, deltaTime)
		wr2.writerow(testResult) # write testresult to *Performance.csv
		t = t - deltaTime			
		# handling response
		if APElib.is_json(r.text):
			jsonDetails = json.loads(r.text)
		else:
			print(r.text)
			break
		data = (i,) # create list with result
		data = data + (jsonDetails['content']['control']['recordId']['value'],)
		data = data + (jsonDetails['content']['cpfDescription']['identity']['nameEntryParallelOrNameEntry'][0]['part'][0]['content'],)
		wr1.writerow(data) # write result to *Result.csv
		i = i + 1

print("\n")
searchresult.close()
testresult.close()

