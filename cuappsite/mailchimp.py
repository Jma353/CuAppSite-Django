import requests 
import json
from requests.auth import HTTPBasicAuth


def get_lists(api_key, list_id, number): 
	url = "https://us" + str(number) + ".api.mailchimp.com/3.0/lists?fields=lists.name,lists.id"
	headers = { "content-type" : "application/json" }

	r = requests.get(url, auth=HTTPBasicAuth('anystring', api_key), headers=headers, verify=True)

	for list in r.json()['lists']:
		print list



def add_member_to_list(api_key, list_id, number, EMAIL, FNAME="", LNAME=""): 
	# API endpoint to add a user 
	url = "https://us" + str(number) + ".api.mailchimp.com/3.0/lists/" + list_id + "/members/"

	info = {
		'email_address': EMAIL, 
		'status': 'subscribed',
		'merge_fields': {
			'FNAME': FNAME,
			'LNAME': LNAME
		}
	}

	headers = { 'content-type' : 'application/json' }

	r = requests.post(url, auth=HTTPBasicAuth('anystring', api_key), headers=headers, verify=True, data=json.dumps(info))




