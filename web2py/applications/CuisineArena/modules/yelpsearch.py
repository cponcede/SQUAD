#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

class YelpSearch():
    # Authenticates the app for calls to the Yelp API
    # https://github.com/Yelp/yelp-python for info on interacting with the Yelp API
    def authenticate_yelp(self):
        from yelp.client import Client
        from yelp.oauth1_authenticator import Oauth1Authenticator

        auth = Oauth1Authenticator(
            consumer_key='HJemwQtFa0nNFxcMA9yu6Q',
            consumer_secret='G5pSWI9eN0ee3O1N2fm3xYE4ais',
            token='YBxSugCSzVpmwCwGswmHv1GCTpfky3VU',
            token_secret='y2UYcyhLG-QEmoadn3Lp6Vnp3nk'
        )
        client = Client(auth)
        return client

    
    def get_restaurant_list(self, cuisineRatings, zipCode, maxDistance, pricePrefs):
        # Use cuisineRatings, zipCode, maxDistance, and pricePrefs to query Yelp API
        yelp_client = self.authenticate_yelp()

        search_params = {'term': 'restaurants',    # only interested in restaurants
                         'sort': 2,               # sort results by highest rating
                         'category_filter': 'chinese,japanese,italian',   # Insert our own cuisines eventually
                         'radius_filter': 40000,       # max distance (in meters)
                        }
        results = yelp_client.search('94305', search_params)

        # Convert results from Yelp API into a list of dictionarys (just returning entire results for now)
        filteredResult = []
        for business in results.businesses:
            business_info = {}
            business_info['name'] = business.name
            business_info['rating'] = business.rating
            business_info['url'] = business.url
            business_info['categories'] = business.categories
            business_info['address'] = business.location.display_address
            filteredResult.append(business_info)
        return filteredResult
