#!/usr/bin/env python 

from lxml import html 
import requests 

def email_to_netid(email): 
	email_array = email.split('@')
	return email_array[0]

# Function returns the name of a Cornell student via a netID.
def get_full_name(email): 
	netID = email_to_netid(email)

	page = requests.get("https://www.cornell.edu/search/people.cfm?netid=" + netID)

	tree = html.fromstring(page.content)

	name = tree.xpath('//h3[@class="cu-headline"]/text()')

	if len(name) > 0: 
		return name[0]
	else: 
		return None 


# Function returns the first name of a Cornell student via a netID 
def get_first_name(netID): 
	full_name = get_full_name(netID)
	if full_name != None: 
		first_name = full_name.split(' ')[0]
		return first_name 

	return full_name # None if not a thing 


# Functions returns the last name of a Cornell student via a netID 
def get_last_name(netID): 
	full_name = get_full_name(netID)
	if full_name != None: 
		name_as_array = full_name.split(' ')
		return name_as_array[len(name_as_array)-1] # Return the last element 
	return full_name # None if not a thing 
