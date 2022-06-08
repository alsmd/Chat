import json
import bcrypt
import jwt
import boto3
from botocore.exceptions import ClientError
import os

dynamodb = boto3.client("dynamodb")
tableName = os.environ['tableName']

def handler(event, context):
	mySalt = bcrypt.gensalt()
	body = json.loads(event['body'])
	username = body.get("username")
	password = body.get("password")
	if not username or not password:
		return defaultResponse(400, {"message": "missing username or password", "created": False})
	hash = bcrypt.hashpw(password.encode("utf-8"), mySalt)
	try:
		dynamodb.put_item(
			TableName = tableName,
			Item = {
				'pk': {
					'S': "USER#" + username
				},
				'sk': {
					'S': "USER"
				},
				'password': {
					'S': hash.decode("utf-8")
				},
				'username': {
					'S': username
				}
			},
			ConditionExpression = 'attribute_not_exists(pk)'
		)
		token = jwt.encode({"username": username}, os.environ['SECRET_KEY'], algorithm="HS256")
		return defaultResponse(200, {"token": token, "created": True})
	except ClientError as error:
		print(error)
		if error.response['Error']['Code'] == 'ConditionalCheckFailedException':
			return defaultResponse(400, {"message": "User alredy exists", "created": False})
		return defaultResponse(400, {"message": "Something went wrong", "created": False})
	
def defaultResponse(status, data = {}):
	return {
		"headers": {
			"Content-Type": "application/json",
			"Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, POST, DELETE, OPTIONS",
			"Access-Control-Allow-Origin": "*",
			"Access-Control-Allow-Credentials": True,
			"Access-Control-Allow-Headers": "x-requested-with, Content-Type, origin, authorization, accept, client-security-token"
		},
		"statusCode": status,
		"body": json.dumps(data)
	}