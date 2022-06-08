import json

data = {
	"1": {
		"name": "Flavio",
		"age": 25,
		"job": "random"
	},
	"2": {
		"name": "Gabriel",
		"age": 44,
		"job": "random"
	},
	"3": {
		"name": "Paulo",
		"age": 19,
		"job": "random"
	}
}

def handler(event, context):
	print(event)

	if not event["pathParameters"] or not event["pathParameters"]["ID"]:
		return defaultResponse(400, {"message": "missing the id from the path"})
	id = event["pathParameters"]["ID"]
	if data.get(id):
		return defaultResponse(200, data.get(id))
	return defaultResponse(400, {"message": "id not found"})

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