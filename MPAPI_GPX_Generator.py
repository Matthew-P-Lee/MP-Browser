#!/usr/bin/env python3

'''
    File name: MPAPI_GPX_Generator
    Author: Matthew Lee - matthew.lee@ridgeline-analytics.com
    Date created: 6/8/2020
    Date last modified: 6/8/2020
    Python Version: 3
    Description: A script that creates a GPX file from MountainProject todo lists.
'''

import urllib.request
import gpxpy.gpx as gpx
import simplejson as json
from decimal import *

mp_URL_base='https://www.mountainproject.com/data'
mp_URL_email='xxx'
mp_private_key='xxxx'

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return Decimal(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#function to return a Python obj from a JSON result via HTTP
def getMP_API(url):
	json_str = urllib.request.urlopen(url).read()
	return json.loads(json_str)
	
#formatted Mountain Project API URL	
def getMP_URL(mp_URL_base,mp_command,mp_URL_email,mp_private_key):
	return str.format("{0}/{1}?email={2}&key={3}",mp_URL_base,mp_command,mp_URL_email,mp_private_key)

#conditional load of the user profile
profile_url = getMP_URL(mp_URL_base,'get-user',mp_URL_email,mp_private_key)
mp_profile = getMP_API(profile_url)

print('Getting MP ToDo List for',mp_profile['name'])

todos_url = getMP_URL(mp_URL_base,'get-to-dos',mp_URL_email,mp_private_key)
mp_todos = getMP_API(todos_url)

#get routes returns an array of integer route Ids, make a string to pass to MP
route_ids = ','.join(str(todo) for todo in mp_todos['toDos'])

if len(route_ids) > 0:	
	#return routes
	routes_url = getMP_URL(mp_URL_base,'get-routes',mp_URL_email,mp_private_key)
	routes_url = str.format("{0}&routeIds={1}",routes_url,route_ids)

	mp_routes = json_str = getMP_API(routes_url)

	gpxinstance = gpx.GPX()

	for route in mp_routes['routes']:
		#print(route)
		#print(route['name'],' - ', route['rating'],' - ',route['location'][1], ' - ' ,route['location'][2])
		#print('latitude', route['latitude'])
		#print('longitude', route['longitude'])
		#print(route['url'])

		gpxinstance.waypoints.append(
			gpx.GPXWaypoint(
				Decimal(str(route['latitude'])), 
				Decimal(str(route['longitude'])), 
				name=route['name'] + ' - ' + route['rating'],
				description=route['url']))

	#write to file
	fo = open(r"todos.gpx", "w+")
	fo.write(gpxinstance.to_xml())
	print('Success: Created GPX File: todos.gpx')
