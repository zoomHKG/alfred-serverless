#!/usr/bin/env python3
"""Alfred Repository Class"""
import logging
import json
import boto3
from requests import get, exceptions

_LOGGER = logging.getLogger(__name__)


class Repository():
    """ALfred repository"""

    def __init__(self):
        """Repository Constructor"""
        self.bucket = 'rpidanny.alfred'
        self.moviesKey = 'alfred/movies.json'
        self.notifiedKey = 'alfred/notified.txt'
        self.s3 = boto3.resource('s3')
        self.notified = self.load_notified()

    def load_notified(self):
        """Load already notified movies from file"""
        """Get movies/emails from repo"""
        try:
            obj = self.s3.Object(self.bucket, self.notifiedKey)
            return obj.get()['Body'].read().decode('utf-8').splitlines()
        except:
            self.s3.Bucket(self.bucket).put_object(
                Key=self.notifiedKey, Body=''.encode('utf-8'))
            return []

    def save_notified(self, movie):
        """append notified movie to file"""
        self.notified.append(movie)
        try:
            self.s3.Bucket(self.bucket).put_object(
                Key=self.notifiedKey, Body='\n'.join(self.notified).encode('utf-8'))
        except:
            return []

    def get_movies(self):
        """Get movies/emails from repo"""
        try:
            obj = self.s3.Object(self.bucket, self.moviesKey)
            data = obj.get()['Body'].read().decode('utf-8')
            movies = json.loads(data)
            return movies
        except ValueError as error:
            _LOGGER.exception(
                'Could not parse JSON content: %s')
            return {}
        except TypeError as error:
            _LOGGER.exception('Failed to serialize to JSON')
            return {}
        except:
            return {}
