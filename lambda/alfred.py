import os
import boto3
import json
import logging
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

    if not (email and passwd and bucket and mkey and nkey):
        exit(1)
    return email, passwd, bucket, mkey, nkey


def main(event, context):
    emailaddr, passwd, bucket, mkey, nkey = get_envs()
    email = Email(emailaddr, passwd)
    repo = Repository(bucket, mkey, nkey)
    yts = YTS()
    wish_list = repo.get_movies()
    available = yts.get_movies()
    notified = []
    for movie in wish_list:
        _LOGGER.debug('{} : {}'.format(movie, movie in available))
        if movie in available:
            _LOGGER.debug('{} Movie available. Sending email.'.format(movie))
            email.send_mail(wish_list[movie], 'Movie Available',
                            'The movie {} is now available on YTS.'.format(movie))
            notified.append(movie)
    if len(notified) > 0:
        repo.save_notified(notified)
    # email.send_mail(['abhishekmaharjan1993@gmail.com'],
    #                 'Awake', "I'm awake!! {}".format(', '.join(movies)))
    
    return response({
        'available': available,
        'wishlist': wish_list,
        'notified': repo.notified
    }, 200)
