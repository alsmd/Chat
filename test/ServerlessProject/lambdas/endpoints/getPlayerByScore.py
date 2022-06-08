import boto3
from boto3.dynamodb.conditions import Key
import json
from botocore.exceptions import ClientError



dynamodb = boto3.client("dynamodb")
tableName = "player-points"
def handler(event, context):
	if not event["pathParameters"] or not event["pathParameters"]["SCORE"]:
		return defaultResponse(400, {"message": "missing the score from the path"})
	score = event["pathParameters"]["SCORE"]
	try:
		response = dynamodb.query(
			TableName=tableName,
			IndexName='Score-index',
			ExpressionAttributeValues={
				':v1': {
					'S': score,
				},
			},
			KeyConditionExpression='Score = :v1'
		)
		items = response.get('Items')
		if not items:
			return defaultResponse(400, {"message": "Could not retrive player's by score"})
		return defaultResponse(200, items) 
	except ClientError as error:
		return defaultResponse(400, {"message": "Something went wrong", "error": error})

def defaultResponse(status, data = {}):
	return {
		"headers": {
			"Content-Type": "application/json",
			"Access-Control-Allow-Methods": "*",
			"Acess-Control-Allow-Origin": "*"
			
		},
		"statusCode": status,
		"body": json.dumps(data)
	}