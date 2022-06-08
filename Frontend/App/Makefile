
BUCKET_NAME = mychatsite-flav



deploy:
	ng build
	# aws s3api remove-bucket --bucket $(BUCKET_NAME)
	aws s3api create-bucket --bucket $(BUCKET_NAME) 
	aws s3api put-bucket-policy --bucket $(BUCKET_NAME) --policy file://bucket_policy.json
	aws s3 cp ./dist/app/ s3://$(BUCKET_NAME)/ --recursive
	aws s3 website s3://$(BUCKET_NAME)/ --index-document index.html --error-document index.html
