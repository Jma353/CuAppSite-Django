import requests 
import json 
from requests.auth import HTTPBasicAuth


def post_message(token, channel, text, username): 
	url = "https://slack.com/api/chat.postMessage"
	headers = { 'content-type' : 'application/json'}
	params = { 
							'token' : token,
							'channel' : channel,
							'text': text,
							'username': username, 
							'icon_emoji': ':eggplant:'
					 }
	r = requests.post(url, headers=headers, params=params, verify=True)
	 



def groups_list(token): 
	url = "https://slack.com/api/groups.list"
	headers = { 'content-type': 'application/json' }
	params = { 'token' : token }
	r = requests.get(url, headers=headers, params=params, verify=True)
	if r.json()['ok'] == True: 
		for group in r.json()['groups']:
			print group
			print "\n"
	else: 
		print r.json()['error']




