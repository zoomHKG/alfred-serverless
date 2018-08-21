# alfred-serverless

Serverless implementation of [Alfred](https://github.com/zoomHKG/alfred)

## Setup

### Requirements

- [AWS lambda](https://aws.amazon.com/lambda) function
- [AWS S3](https://aws.amazon.com/s3) bucket

### Installation

```shell
pip install beautifulsoup4==4.6.0 requests==2.19.1 -t ./lambda/
```

### Deployment

- Change the function name in `deploy.sh` to your function name.
- Add `EMAIL`, `PASSWD`, `YTS`, `BUCKET`, `MOVIES`, `NOTIFIED` Environment Variables to your lambda function.
- run `./deploy.sh`
- Configure `triggers` to your deployed function. (`API Gateway` or `CloudWatch Events` maybe?)
