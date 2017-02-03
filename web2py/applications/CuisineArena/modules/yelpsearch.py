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

    # Queries Yelp API for restaurants that match the provided arguments and returns information about matching restaurants.
    # Parameters:
    #     cuisineRatings : dict from String(cuisineName) -> Double(cuisineRating). Used to filter results based on CuisineArena results
    #     zipCode: String representation of user's zip code
    #     maxDistance: maximum distance (in meters) that the user wants results fro
    #     pricePrefs: Dict that looks like: {'$': Bool, '$$': Bool, '$$$': Bool} that is used to determine which price ranges to consider
    def get_restaurant_list(self, cuisineRatings, zipCode, maxDistance, pricePrefs):
        yelp_client = self.authenticate_yelp()

        category_string = "restaurants,"
        for cuisine_name in cuisineRatings.keys():
            category_string = category_string + cuisine_name + ','
        category_string = category_string[:-1] # remove last comma
        print category_string

        search_params = {'term': 'restaurants',    # only interested in restaurants
                         'category_filter': category_string,   # Insert our own cuisines eventually
                         'radius_filter': maxDistance,       # max distance (in meters)
                        }
        results = yelp_client.search(zipCode, search_params)

        # No application of cuisine ratings or price prefs used here yet. 
        # Just simply returns results for all listed cuisine types, sorted by rating.
        filteredResult = []
        for business in results.businesses:
            if 'japanese' not in business.categories:
                continue
            business_info = {}
            business_info['name'] = business.name
            business_info['rating'] = business.rating
            business_info['url'] = business.url
            business_info['categories'] = business.categories
            business_info['address'] = business.location.display_address
            filteredResult.append(business_info)
        return filteredResult
