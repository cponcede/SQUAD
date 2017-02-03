#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

class RestaurantSearch():
    
    # Queries Factual API and returns results based on inputted arguments.
    # Parameters:
    #     location - zip code of the user
    #     max_distance - maximum distance (in meters) to find results within
    #     category_ratings - dictionary from String(category name) -> Double (rating)
    #     price_prefs - dictionary from String($ amount) -> Bool (whether or not to look in that range)
    def get_restaurants(self, location, max_distance, category_ratings, price_prefs):
        # TODO: Query Factual API once we get approved for access
        hard_coded_results = []
        hard_coded_restaurant = {}
        hard_coded_restaurant['name'] = 'Fake Restaurant'
        hard_coded_restaurant['rating'] = 4.2
        hard_coded_results.append(hard_coded_restaurant)
        return hard_coded_results

    # Queries Factual API based on the provided Factual restaurant ID and returns a
    # dictionary of information about that restaurant.
    def get_restaurant_details(self, restaurant_factual_id):
        # TODO: Query Factual API to get restaurant details once we have access
        hard_coded_restaurant_details = {}
        hard_coded_restaurant_details['name'] = 'Fake Restaurant'
        hard_coded_restaurant_details['rating'] = 4.2
        # TODO: Include much more info once I have the factual API available
        return hard_coded_restaurant_details
