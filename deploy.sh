cd lambda
zip -r ../alfred.zip *
cd ..
aws lambda update-function-code \
  --profile useast1 \
  --function-name alfred \
  --zip-file fileb://alfred.zip
