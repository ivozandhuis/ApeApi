import json

# config

server = "ACC"
keyFor = "ACC"

def setBaseurl():
	if server == "ACC":
		# acceptance
		base_url = "https://acceptance.archivesportaleurope.net/ApeApi/services"
	if server == "CCH":
		# contentchecker
		base_url = ""
	if server == "PRO":
		# production
		base_url = "https://api.archivesportaleurope.net/services"
	return base_url

def setAPIkey():
	if keyFor == "EMPTY":
		# development
		APIkey = ''
	if keyFor == "ACC":
		# acceptance
		APIkey = 'get_your_key'
	if keyFor == "CCH":
		# contentchecker
		APIkey = 'get_your_key'
	if keyFor == "PRO":
		# production
		APIkey = 'get_your_key'
	return APIkey

def setAccept():
	if server == "ACC":
		# acceptance
		accept = 'application/vnd.ape-v2+json; charset=utf8'
	if server == "CCH":
		# contentchecker
		accept = 'application/vnd.ape-v2+json; charset=utf8'
	if server == "PRO":
		# production
		accept = 'application/vnd.ape-v2+json; charset=utf8'
	return accept

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError:
    return False
  return True
