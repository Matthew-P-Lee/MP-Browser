import json
import boto3
import decimal
import sys
from flask import Flask
from flask import jsonify
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'MP-Browser'

@app.route('/user/<int:user_id>')
def show_user_profile(user_id):
	
	client = boto3.resource('dynamodb')
	
	tbl_users = client.Table('User')
    
	response = tbl_users.get_item(
		Key={
			"UserId": int(user_id)
		}
	)    
	
	item = response.get('Item',0)	
	
	#use this to return the JSON string to the screen
	return app.response_class(json.dumps(item,cls=DecimalEncoder), content_type='application/json')

	#return app.response_class((item), content_type='application/json')
	
@app.route('/route/<int:route_id>')
def show_route(route_id):
	
	client = boto3.resource('dynamodb')
	tbl_routes = client.Table('Routes')
    
	response = tbl_routes.get_item(
		Key={
			"RouteId": int(route_id)
		}
	)    
		
	item = response.get('Item',0)	
	
	#use this to return the JSON string to the screen
	return app.response_class(json.dumps(item,cls=DecimalEncoder), content_type='application/json')

	#return app.response_class((item), content_type='application/json')	

@app.route('/user/ticks/<int:user_id>')	
def show_ticks_for_user(user_id):
	#show list of ticks for a user
	client = boto3.resource('dynamodb')
	tbl_ticks = client.Table('Ticks')
	
	response = tbl_ticks.query(
	   KeyConditionExpression=Key('UserId').eq(user_id)
	)
		
	item = response.get('Items',0)	
	
	#use this to return the JSON string to the screen
	return app.response_class(json.dumps(item,cls=DecimalEncoder), content_type='application/json')
	#return app.response_class((response), content_type='application/json')	
	#return jsonify(response)
	
if __name__ == '__main__':
    app.run()