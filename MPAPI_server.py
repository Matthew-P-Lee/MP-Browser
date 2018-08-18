import json
import boto3
import decimal
import sys
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from boto3.dynamodb.conditions import Key, Attr
from MPAPI_classes import *

# Helper class to convert a DynamoDB item to JSON.  For some reason Boto has trouble 
# time dealing with floats in JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#use this to return the JSON string to the screen
def get_JSON(item):
	return app.response_class(json.dumps(item,cls=DecimalEncoder), content_type='application/json')

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
MPAPI = MPAPI()

@app.route('/')
def show_login():
    return 'Welcome to MP-Browser'

@app.route('/user/<int:user_id>')
def show_user_profile(user_id):
	item = MPAPI.get_profile(user_id)
	return get_JSON(item)
	
@app.route('/route/<int:route_id>')
def show_route(route_id):	
	item = MPAPI.get_route(route_id)
	return get_JSON(item)

@app.route('/user/ticks/<int:user_id>')	
def show_ticks_for_user(user_id):	
	item = MPAPI.get_ticks(user_id)
	return get_JSON(item)
	
if __name__ == '__main__':
    app.run()