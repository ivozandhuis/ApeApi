import json

# config

def setBaseurl():
	base_url = "https://api.archivesportaleurope.net/services"
	return base_url

def setAPIkey():
	APIkey = 'get_your_own_APIkey'
	return APIkey

def setAccept():
	accept = 'application/vnd.ape-v2+json; charset=utf8'
	return accept

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError:
    return False
  return True
