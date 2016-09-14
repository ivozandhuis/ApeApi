#! /usr/bin/env python3

serviceToTest = '/search/eac-cpf'

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

# setting up CSV files
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

filename1 = 'searchEacFacetResult' + st + '.csv'
filename2 = 'searchEacFacetPerformance' + st + '.csv'

searchresult = open(filename1, 'w')
wr1 = csv.writer(searchresult, quoting=csv.QUOTE_ALL)
wr1.writerow(("facet","id","name","frequency"))
testresult = open(filename2, 'w')
wr2 = csv.writer(testresult, quoting=csv.QUOTE_ALL)
wr2.writerow(("index","url","size (bytes)","time (ms)"))

# create request
url = base_url + serviceToTest
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
# handling response
if APElib.is_json(r.text):
	jsonResultlist = json.loads(r.text)
else:
	print(r.text)

facetFields = jsonResultlist['facetFields']
facetList = ['country','repository','entityType','place','language','dateType']

for facetItem in facetList:
	facet = facetFields[facetItem]
	for item in facet:
		data = (facetItem,)
		data = data + (item['id'],)
		data = data + (item['name'],)
		data = data + (item['frequency'],)
		wr1.writerow(data) # write result to *Result.csv

facetFields = jsonResultlist['facetDateFields']
facetList = ['fromDate','toDate']

for facetItem in facetList:
	facet = facetFields[facetItem]
	for item in facet:
		data = (facetItem,)
		data = data + (item['id'],)
		data = data + (item['name'],)
		data = data + (item['frequency'],)
		wr1.writerow(data) # write result to *Result.csv

print("\n")
searchresult.close()
testresult.close()

