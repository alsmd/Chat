import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client("dynamodb")
tableName = "player-points"
def handler(event, context):
	print(event)
	print(context)
	if not event["pathParameters"] or not event["pathParameters"]["ID"]:
		return defaultResponse(400, {"message": "missing the id from the path"})
	id = event["pathParameters"]["ID"]
	try:
		response = dynamodb.get_item(
			TableName = tableName,
			Key = {
				'ID': {
					'S': id
				}
			},
			ProjectionExpression = "ID, Score"
		)
		if not response:
			return defaultResponse(400, {"message": "Could not retrive player's score"})
		if not response.get("Item"):
			return defaultResponse(400, {"message": "Player doenst exists"})
		return defaultResponse(200, response["Item"]) 
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