import json
from sqlite3 import connect
import jwt
import boto3
from botocore.exceptions import ClientError
import os
import uuid

dynamodb = boto3.client("dynamodb")
tableName = os.environ['tableName']

def handler(event, context):
	auth_token = event["headers"].get('Authorization')
	if not auth_token:
		return defaultResponse(400, {"connected": False,"message": "You need to provide jwt token"})
	user = checkToken(auth_token)
	if not user:
		return defaultResponse(400, {"connected": False,"message": "Invalid Token"})
	body = json.loads(event['body'])
	connectWith = body.get("connectWith")
	if not connectWith:
		return defaultResponse(400, {"connected": False, "message": "Missing connectWith"})
	chatId = getChat(user.get("username"), connectWith)
	if chatId:
		return defaultResponse(200, {"connected": True, "chatId": chatId})
	return createChat(user.get("username"), connectWith)
		

def createChat(username, connectWith):
	try:
		chatId = str(uuid.uuid4())
		dynamodb.put_item(
			TableName = tableName,
			Item = {
				'pk': {
					'S': "CHAT#" + username + "#" + chatId
				},
				'sk': {
					'S': "WITH#" + connectWith
				}
			},
			ConditionExpression = 'attribute_not_exists(pk)'
		)
		dynamodb.put_item(
			TableName = tableName,
			Item = {
				'pk': {
					'S': "CHAT#" + connectWith + "#" + chatId
				},
				'sk': {
					'S': "WITH#" + username
				}
			},
			ConditionExpression = 'attribute_not_exists(pk)'
		)
		return defaultResponse(200, {"chatId": chatId, "connected": True})
	except ClientError as error:
		print(error)
		return defaultResponse(400, {"message": "Something went wrong", "connected": False})


def getChat(username, connectWith):
	try:
		response = dynamodb.query(
			TableName=tableName,
			IndexName='sk-index',
			ExpressionAttributeValues={
				':v1': {
					'S': 'WITH#' + connectWith,
				},
				':v2': {
					'S': "CHAT#" + username
				}
			},
			KeyConditionExpression='sk = :v1 and begins_with(pk, :v2)',
			ProjectionExpression = "pk"
		)
		item = response.get('Items')
		if not item:
			return
		item = item[0]
		if not item or not item["pk"] or not item["pk"]["S"]:
			return
		chatId = item["pk"]["S"].split("#")[2]	
		return chatId
	except ClientError as error:
		print(error)
		return


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