import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

# common functions for the web service
# mostly just handles DynamoDB in/out
class MPAPI():
	def __init__(self):
		return
		
	#gets a single user profile
	def get_profile(self, user_id):
		
		client = boto3.resource('dynamodb')

		tbl_users = client.Table('User')

		response = tbl_users.get_item(
			Key={
				"UserId": int(user_id)
			}
		)    
			
		item = response.get('Item',0)	
	
		return item 
	
	#gets a single route
	def get_route(self,route_id):
		
		client = boto3.resource('dynamodb')
		tbl_routes = client.Table('Routes')
		    
		response = tbl_routes.get_item(
			Key={
				"RouteId": int(route_id)
			}
		)    
				
		item = response.get('Item',0)	
		
		return item
		
	#returns ticks with routes	
	def get_ticks(self,user_id):
		
		#show list of ticks for a user
		client = boto3.resource('dynamodb')
		tbl_ticks = client.Table('Ticks')
		
		response = tbl_ticks.query(
		   KeyConditionExpression=Key('UserId').eq(user_id)
		)
	
		item = response.get('Items',0)
				
		#append the route information
		for route in item:			
			routeinfo = MPAPI().get_route(int(route['RouteId']))	
			route.update(routeinfo)
			
		return item