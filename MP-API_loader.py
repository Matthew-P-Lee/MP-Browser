import urllib.request
import json
import boto3
import decimal

mp_URL_base='https://www.mountainproject.com/data'
mp_URL_email='matt@vistaseeker.com'
mp_private_key='112244155-faf71266e0e5a4f73c53cc5ef291800d'

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
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

client = boto3.resource('dynamodb')

#conditional load of the user profile
profile_url = getMP_URL(mp_URL_base,'get-user',mp_URL_email,mp_private_key)
mp_profile = getMP_API(profile_url)

tbl_users = client.Table('User')
user_id = mp_profile['id']

#store these to load routes (should requery)
response = tbl_users.get_item(
		Key={
			"UserId": user_id
		}
	)

item = response.get('Item',0)

#check to see if the route already exists then insert the tick into DDB
if (item == 0):
	print("Adding User ",str(mp_profile['name']))
	tbl_users.put_item(
		Item={
			'UserId':  user_id,
			'name': mp_profile['name']
		}
	)
else:
	print('Skipping User for',str(user_id))


#Conditional Load of the Ticks Table 
tbl_ticks = client.Table('Ticks')
	
ticks_url = getMP_URL(mp_URL_base,'get-ticks',mp_URL_email,mp_private_key)
mp_ticks = getMP_API(ticks_url)
route_Ids = []

for tick in mp_ticks['ticks']:
	
	route_id = tick['routeId']
	
	#store these to load routes (should requery)
	route_Ids.append(str(route_id))
	

	response = tbl_ticks.get_item(
			Key={
				"RouteId": int(route_id),
				"UserId": int(user_id)
			}
		)

#	item = 0	
	item = response.get('Item',0)
	
	#check to see if the route already exists then insert the tick into DDB
	if (item == 0):
		print("Adding Tick for",str(route_id))
		tbl_ticks.put_item(
			Item={
				'RouteId': route_id,
				'date': tick['date'],
				'UserId': user_id
			}
		)
	else:
		print('Skipping Tick for',str(route_id))

#Conditional Load of the Routes Table
tbl_routes = client.Table('Routes')

#return all routes
routes_url = getMP_URL(mp_URL_base,'get-routes',mp_URL_email,mp_private_key)
routes_url = str.format("{0}&routeIds={1}",routes_url,str.join(",",route_Ids))

mp_routes = json_str = getMP_API(routes_url)

for route in mp_routes['routes']:
	route_id = route['id']
		
	response = tbl_routes.get_item(
			Key={
				"RouteId": route_id
			}
		)
		
	item = response.get('Item',0)
	
	#check to see if the route already exists then insert the tick into DDB
	if (item == 0):
		print("Adding Route",route['name'])
		tbl_routes.put_item(
			Item={
				'RouteId': route_id,
				'name': route['name'],
				'rating': route['rating'],
				'state': route['location'][0],
				'area': route['location'][1],
				'location': route['location'][3]
			}
		)
	else:
		print("Skipped Route",route['name'])
