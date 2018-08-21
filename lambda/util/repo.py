#!/usr/bin/env python3
"""Alfred Repository Class"""
import logging
import json
import boto3
from requests import get, exceptions

_LOGGER = logging.getLogger(__name__)


class Repository():
    """ALfred repository"""

    def __init__(self, bucket, movieKey, notifiedkey):
        """Repository Constructor"""
        self.bucket = bucket
        self.mKey = movieKey
        self.nKey = notifiedkey
        self.s3 = boto3.resource('s3')
        self.notified = self.load_notified()

    def load_notified(self):
        """Load already notified movies from file"""
        """Get movies/emails from repo"""
        try:
            obj = self.s3.Object(self.bucket, self.nKey)
            return obj.get()['Body'].read().decode('utf-8').splitlines()
        except:
            self.s3.Bucket(self.bucket).put_object(
                Key=self.nKey, Body=''.encode('utf-8'))
            return []

    def save_notified(self, movies):
        """append notified movie to file"""
        self.notified += movies
        try:
            self.s3.Bucket(self.bucket).put_object(
                Key=self.nKey, Body='\n'.join(self.notified).encode('utf-8'))
        except:
            return []

    def get_movies(self):
        """Get movies/emails from repo"""
        try:
            obj = self.s3.Object(self.bucket, self.mKey)
            data = obj.get()['Body'].read().decode('utf-8')
            movies = json.loads(data)
            filtered_movies = dict((k, v) for k, v in movies.items() if k not in self.notified)
            return filtered_movies
        except ValueError as error:
            _LOGGER.exception(
                'Could not parse JSON content: %s')
            return {}
        except TypeError as error:
            _LOGGER.exception('Failed to serialize to JSON')
            return {}
        except:
            return {}
