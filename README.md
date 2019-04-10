# alfred-serverless

A [Serverless](https://serverless.com) application that checks for new movies on YTS (other sources to be added soon) and notifies the subscribers of [alfred-repository](https://github.com/zoomHKG/alfred-repository) by email.

## Requirements

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [Serverless](https://serverless.com)

## Setup

1. `aws ssm put-parameter --name github-key --type String --value $GITHUB_KEY --profile default --overwrite --region eu-west-1`
2. `aws ssm put-parameter --name github-username --type String --value $GITHUB_USER --profile default --overwrite --region eu-west-1`
3. `aws ssm put-parameter --name github-email --type String --value $GITHUB_EMAIL --profile default --overwrite --region eu-west-1`

## Deploy

`npm run deploy`
