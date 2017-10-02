zip -r archive.zip *
aws lambda update-function-code --function-name=IsolationBot --zip-file=fileb://archive.zip
