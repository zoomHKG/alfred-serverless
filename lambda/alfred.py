import os
import boto3
import json
import logging
import util.mailer
from util.email import Email
from util.repo import Repository
from util.yts import YTS

_LOGGER = logging.getLogger(__name__)


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
    email = os.environ.get('EMAIL')
    passwd = os.environ.get('PASSWD')
    bucket = os.environ.get('BUCKET')
    mkey = os.environ.get('MOVIES')
    nkey = os.environ.get('NOTIFIED')
    mailer_url = os.environ.get('MAILER_URL')

    if not (email and passwd and bucket and mkey and nkey and mailer_url):
        exit(1)
    return email, passwd, bucket, mkey, nkey


def main(event, context):
    # get app configs
    emailaddr, passwd, bucket, mkey, nkey = get_envs()

    # initialize objects
    repo = Repository(bucket, mkey, nkey)
    yts = YTS()

    # get necessary movie data
    wish_list = repo.get_movies()
    available = yts.get_movies()
    notified = []

    # check if wanted movie available
    for movie in wish_list:
        _LOGGER.debug('{} : {}'.format(movie, movie in available))
        if movie in available:
            _LOGGER.debug('{} Movie available. Sending email.'.format(movie))
            mailer.send_mail(wish_list[movie], 'Movie Available',
                            'The movie {} is now available on YTS.'.format(movie))
            notified.append(movie)
    
    # update notified list
    if len(notified) > 0:
        repo.save_notified(notified)
    # mailer.send_mail(['abhishekmaharjan1993@gmail.com'],
    #                 'Awake', "I'm awake!! {}".format(', '.join(wish_list)))
    
    return response({
        'available': available,
        'wishlist': wish_list,
        'notified': repo.notified
    }, 200)
