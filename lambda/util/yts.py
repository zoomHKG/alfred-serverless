#!/usr/bin/env python3
"""yts.ag scrapping stuffs here"""
import os
import requests
from bs4 import BeautifulSoup


class YTS():
    """Class for YTS scrapping"""

    def __init__(self):
        """Constructor"""
        # self.url = os.environ.get("YTS", 'https://yts.am/')
        self.url = os.environ.get("YTS", 'http://127.0.0.1:8080/')
        self.previous = []

    def get_page(self):
        """fetch and parse yts homepage"""
        source_code = requests.get(self.url)
        plain_text = source_code.text
        return BeautifulSoup(plain_text, "html.parser")


    def get_latest(self):
        """get latest movies"""
        latest_movies = []
        soup = self.get_page()
        latest_parent = soup.find('div', {'class': 'home-movies'})
        latest_child_div = latest_parent.findAll('div', {'class': 'browse-movie-wrap'})
        for elem in latest_child_div:
            movie_name_div = elem.find('div', {'class': 'browse-movie-bottom'})
            movie_name = movie_name_div.find('a', {'class': 'browse-movie-title'}).text
            latest_movies.append(movie_name)
        return latest_movies


    def get_featured(self):
        """get featured movies"""
        featured_movies = []
        soup = self.get_page()
        featured_parent = soup.find('div', {'id': 'popular-downloads'})
        featured_child_div = featured_parent.findAll('div', {'class': 'browse-movie-wrap'})
        for elem in featured_child_div:
            movie_name_div = elem.find('div', {'class': 'browse-movie-bottom'})
            movie_name = movie_name_div.find('a', {'class': 'browse-movie-title'}).text
            featured_movies.append(movie_name)
        return featured_movies


    def get_movies(self):
        """Generic function to get new movies"""
        latest = self.get_latest()
        featured = self.get_featured()
        final = list(set(latest) | set(featured))
        # diff = list(set(final) - set(self.previous))
        # self.previous = final
        return final
