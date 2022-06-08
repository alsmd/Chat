import json
import jwt
import boto3
from botocore.exceptions import ClientError
import os

dynamodb = boto3.client("dynamodb")
tableName = "ChatTable"#pegar da env em breve
def handler(event, context):
	auth_token = event["headers"].get('Authorization')
	if not auth_token:
		return defaultResponse(400, {"message": "You need to provide jwt token"})
	if not checkToken(auth_token):
		return defaultResponse(400, {"message": "Invalid Token"})
	try:
		resp = dynamodb.query(
			TableName=tableName,
			IndexName='sk-index',
			ExpressionAttributeValues={
				':v1': {
					'S': 'USER',
				},
			},
			KeyConditionExpression='sk = :v1',
			ProjectionExpression = "username"
		)
		items = resp.get('Items')
		return defaultResponse(200, items)
	except ClientError as error:
		print(error)
		return defaultResponse(400, {"message": "Something went wrong"})

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