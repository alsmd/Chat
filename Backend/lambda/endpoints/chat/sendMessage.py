import json
import jwt
import boto3
from botocore.exceptions import ClientError
import os
import time
import uuid


dynamodb = boto3.client("dynamodb")
tableName = os.environ['tableName']

def handler(event, context):
	auth_token = event["headers"].get('Authorization')
	if not auth_token:
		return defaultResponse(400, {"message": "You need to provide jwt token"})
	user = checkToken(auth_token)
	if not user:
		return defaultResponse(400, {"message": "Invalid Token"})
	body = json.loads(event['body'])
	chatId = body.get("chatId")
	message = body.get("message")
	if not chatId or not message:
		return defaultResponse(400, {"message": "missing chatId or message"})
	if not isAtChat(chatId, user.get("username")):
		return defaultResponse(400, {"message": "you don't have permission to post in this chat"})
	try:
		dynamodb.put_item(
			TableName = tableName,
			Item = {
				'pk': {
					'S': "CHAT#" + chatId
				},
				'sk': {
					'S': "MESSAGE#" + str(time.time()) + "#" + str(uuid.uuid4())
				},
				'username': {
					'S': user.get("username")
				},
				'message': {
					'S': message
				}
			}
		)
		return defaultResponse(200, {"message": "message sent succesfuly"})
	except ClientError as error:
		print(error)
		return defaultResponse(400, {"message": "something went wrong"})

def isAtChat(chatId, username):
	try:
		response = dynamodb.query(
			TableName=tableName,
			ExpressionAttributeValues={
				':v1': {
					'S': 'CHAT#' + username + "#" + chatId
				}
			},
			KeyConditionExpression='pk = :v1',
			ProjectionExpression = "pk"
		)
		item = response.get('Items')
		if not item:
			return False
		item = item[0]
		if not item:
			return False
		return True
	except ClientError as error:
		print(error)
		return False

def checkToken(auth_token):
	try:
		auth_token = auth_token.replace('Bearer ', '')
		r = jwt.decode(jwt = auth_token, key = os.environ['SECRET_KEY'], algorithms = "HS256")
		return r
	except jwt.ExpiredSignatureError:
		return
	except jwt.InvalidTokenError:
		return
	
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