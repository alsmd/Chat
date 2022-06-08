import json
import bcrypt
import jwt
import boto3
from botocore.exceptions import ClientError
import os

dynamodb = boto3.client("dynamodb")
tableName = os.environ['tableName']

def handler(event, context):
	# mySalt = bcrypt.gensalt()
	body = json.loads(event['body'])
	username = body.get("username")
	password = body.get("password")
	if not username or not password:
		return defaultResponse(400, {"message": "missing username or password", "token": ""})
	try:
		response = dynamodb.get_item(
			TableName = tableName,
			Key = {
				'pk': {
					'S': "USER#" + username
				},
				'sk': {
					'S': "USER"
				}
			},
			ProjectionExpression = "username, password"
		)
		if not response or not response.get("Item"):
			return defaultResponse(400, {"message": "Could not found user", "token": ""})
		item = response["Item"]
		password = password.encode("utf-8")
		# hash = bcrypt.hashpw(password.encode("utf-8"), mySalt)
		if bcrypt.checkpw(password, item["password"]["S"].encode("utf-8")):
			token = jwt.encode({"username": item["username"]["S"]}, os.environ['SECRET_KEY'], algorithm="HS256")#secret key vira do enviroment
			return defaultResponse(200, {"token": token})
		else:
			return defaultResponse(400, {"message": "Incorret password", "token": ""})
	except ClientError as error:
		print(error)
		return defaultResponse(400, {"message": "Something went wrong", "token": ""})
	

	

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