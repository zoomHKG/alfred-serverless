import os
import boto3
import json
from util.email import Email
from util.repo import Repository

def response(message, status_code):
    return {
        'statusCode': str(status_code),
        'body': json.dumps(message),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
        }

def get_credentials():
    """get email credentials from ENV"""
    email = os.environ.get("EMAIL")
    passwd = os.environ.get("PASSWD")
    if not (email and passwd):
        exit(1)
    return email, passwd

def main(event, context):
    email, passwd = get_credentials()
    email = Email(email, passwd)
    repo = Repository()
    # repo.save_notified('avengers')
    movies = repo.get_movies()
    email.send_mail(['abhishekmaharjan1993@gmail.com'],
                    'Awake', "I'm awake!! {}".format(', '.join(movies)))
    return response({
        'message': movies,
        'notified': repo.notified
    }, 200)