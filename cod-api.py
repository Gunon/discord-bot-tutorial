import requests
import json
import os
import uuid
from requests.auth import HTTPBasicAuth

client = requests.session()
#url = "https://profile.callofduty.com/cod/login"
codUsername="Gunon%237519557"
codEmail="gunon.96@gmail.com"
codPass=os.getenv('COD_PASS')
#leaving this for the moment because screw you COD not documenting your API I just want to build a bot for my friends discord :(


def warzoneDetails():
  version= "v2"
  game="mw"
  gameType="wz"
  platform="battle"
  username="Gunon%231951"
  start="0"
  end="0"
  URL = f"https://my.callofduty.com/api/papi-client/crm/cod/{version}/title/{game}/platform/{platform}/gamer/{username}/matches/{gameType}/start/{start}/end/{end}/details"
  XRFTOKEN_COD = os.getenv('XRFTOKEN_COD')
  payload = {}
  headers = {
    'Cookie': 'XSRF-TOKEN={{'+ XRFTOKEN_COD + '}}'
  }

  response = requests.request("GET", URL, headers=headers, data = payload)

  print(response.text)

  #json_data = json.loads(response.text)

def getCSRF():
  URL = "https://profile.callofduty.com/cod/login"
  
  request = client.get(URL)
  payload = {}
  headers= {}
  if 'XSRF-TOKEN' in client.cookies:
    csrftoken = client.cookies['XSRF-TOKEN']
  else:
    print("NO TOKEN")

  url = "https://profile.callofduty.com/do_login?new_SiteId=cod"
  unique_Id = uuid.uuid4()
  #url = "https://profile.callofduty.com/cod/mapp/"


  payload = {'username': codEmail,
  'password': codPass,
  '_csrf': csrftoken}
  files = [

  ]

  headers = request.headers

  #first_response = requests.request("POST",url+"login", headers=headers, data = payload, files = files)

  response = requests.request("POST", url, headers=headers, data = payload, files = files)
  #response = requests.get(url, auth=HTTPBasicAuth(codEmail, codPass))
  print(response.text)

  return csrftoken

def login(XRFTOKEN_COD):
  url = "https://profile.callofduty.com/do_login?new_SiteId=cod"
  unique_Id = uuid.uuid4()
  #url = "https://profile.callofduty.com/cod/mapp/"


  payload = {'username': codEmail,
  'password': codPass,
  '_csrf': XRFTOKEN_COD}
  files = [

  ]

  headers = {
    'Cookie': f'XSRF-TOKEN={XRFTOKEN_COD}'
  }

  #first_response = requests.request("POST",url+"login", headers=headers, data = payload, files = files)

  #response = requests.request("POST", url, headers=headers, data = payload, files = files)
  response = requests.get(url, auth=HTTPBasicAuth(codEmail, codPass))
  print(response.headers)

XRFTOKEN_COD = getCSRF()
#login(XRFTOKEN_COD)
#warzoneDetails()