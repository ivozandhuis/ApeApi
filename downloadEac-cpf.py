#! /usr/bin/env python3

serviceToTest = '/download/eac-cpf/'

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
APIkey   = APElib.setAPIkey()
accept   = APElib.setAccept()

# create dict header
header = {}
header['accept'] = accept
header['APIkey'] = APIkey

# setting up CSV files
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

filename2 = 'downloadEac-cpfPerformance' + st + '.csv'

testresult = open(filename2, 'w')
wr2 = csv.writer(testresult, quoting=csv.QUOTE_ALL)
wr2.writerow(("index","url","size (bytes)","time (ms)","downloadtime (ms)"))

# --> Change your personal query here:
query = 'louis'

# create dict header
header = {}
header['accept'] = accept
header['APIkey'] = APIkey

# create basic dict payload for POST-requests on /search/eac-cpf
payload = {}
payload['query'] = query
payload['count'] = 5

# requesting and iterating through the results
totalResults = 1 # dummy value to get started...
i = 0 # index, numbering the results
t = 30000 # script runs a maximum of ca. 5 minutes (= 300000 ms)
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
	docs = jsonResultlist['eacSearchResults']	
	for doc in docs:
		# create request
		header['accept'] = ''
		service = serviceToTest
		docId = doc['id']
		url = base_url + service + docId
		print("*", end="", flush=True)

		# do request
		start = time.time() # start measuring response time
		r = requests.get(url, headers=header) # do the request
		end = time.time() # end measuring response time

		# download file
		start2 = time.time() # start measuring download time
		filename1 = docId + '.xml'
		searchresult = open(filename1, 'w')
		searchresult.write(r.text)
		searchresult.close()
		end2 = time.time() # end measuring download time
		
		# calculate measurements
		deltaTime = int((end - start) * 1000)
		deltaTime2 = int((end2 - start2) * 1000)
		size = sys.getsizeof(r.text)
		t = t - deltaTime
		t = t - deltaTime2

		# write log in *Performance.csv
		testResult = (i, url, size, deltaTime, deltaTime2)
		wr2.writerow(testResult) # write testresult to *Performance.csv

	i = i + 1

print("\n")
testresult.close()

