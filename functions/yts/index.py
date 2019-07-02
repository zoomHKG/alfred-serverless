import os
import boto3
import json
from util import mailer
from util.repo import Repository
from util.yts import YTS


def response(message, status_code):
    return {
        'statusCode': str(status_code),
        'body': json.dumps(message),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }


def get_envs():
    """get email credentials from ENV"""
    bucket = os.environ.get('S3_BUCKET')
    mailer_url = os.environ.get('MAILER_URL')

    if not (bucket and mailer_url):
        exit(1)
    return bucket


def main(event, context):
    # get app configs
    bucket = get_envs()

    # initialize objects
    repo = Repository(bucket)
    yts = YTS()

    # get necessary movie data
    wish_list = repo.get_movies()
    available = yts.get_movies()
    notified = []

    # check if wanted movie available
    for movie in wish_list:
        print('{} : {}'.format(movie, movie in available))
        if movie in available:
            print('{} Movie available. Sending email.'.format(movie))
            mailer.send_mail(wish_list[movie], 'Movie Available',
                            'The movie {} is now available on YTS.'.format(movie))
            notified.append(movie)
    
    # update notified list
    if len(notified) > 0:
        repo.save_notified(notified)
    
    return response({
        'available': available,
        'wishlist': wish_list,
        'notified': repo.notified
    }, 200)

def test (event, context):
    mailer.send_mail('whote73@gmail.com', 'Email Test',
                    'Email Works')
