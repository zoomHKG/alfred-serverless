cd lambda
zip ../alfred.zip *
cd ..
aws lambda update-function-code --function-name alfred --zip-file fileb://alfred.zip