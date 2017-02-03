#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import oauth2
import requests

class YelpSearch():
    
    # Queries Yelp API and returns results based on inputted arguments.
    # Parameters:
    #     location - zip code of the user
    #     max_distance - maximum distance (in meters) to find results within
    #     category_ratings - dictionary from String(category name) -> Double (rating)
    #     price_prefs - dictionary from String($ amount) -> Bool (whether or not to look in that range)
    def get_restaurants(self, location, max_distance, category_ratings, price_prefs):
        consumer_key='HJemwQtFa0nNFxcMA9yu6Q'
        consumer_secret='G5pSWI9eN0ee3O1N2fm3xYE4ais'
        token='YBxSugCSzVpmwCwGswmHv1GCTpfky3VU'
        token_secret='y2UYcyhLG-QEmoadn3Lp6Vnp3nk'

        consumer = oauth2.Consumer(consumer_key, consumer_secret)

        category_filter = ""
        for category in category_ratings.keys():
            category_filter = category_filter + category + ','
        category_filter = category_filter[:-1]

        url = 'http://api.yelp.com/v2/search?category_filter=%s&location=%s&sort=2&radius_filter=%s' % (category_filter,location,max_distance)

        oauth_request = oauth2.Request('GET', url, {})
        oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                              'oauth_timestamp': oauth2.generate_timestamp(),
                              'oauth_token': token,
                              'oauth_consumer_key': consumer_key})

        token = oauth2.Token(token, token_secret)

        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)

        signed_url = oauth_request.to_url()
        resp = requests.get(url=signed_url).json()

        filtered_results = []
        businesses = resp['businesses']
        for business in businesses:
            business_info = {}
            business_info['name'] = business['name']
            business_info['categories'] = business['categories']
            business_info['rating'] = business['rating']
            business_info['address'] = business['location']['display_address']
            business_info['url'] = business['url']
            filtered_results.append(business_info)
        return filtered_results
