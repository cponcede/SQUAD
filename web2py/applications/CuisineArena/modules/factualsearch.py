#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import operator

class FactualSearch():
    def searchForRestaurants(self, zipCode, maxDistance, pricePrefs, cuisineRatings):
        # make a call to Factual API to get top 50 rated restaurants in area at desired price point
        # Note: we should only query for restaurants in the top 3 - 5 cuisines. 
        # Hard-code results for now until we have an API key.
        results = [{'name':'Chinese Restaurant', 'rating':5.0, 'cuisine':'chinese', 'id': 'china'},
                   {'name':'Japanese Restaurant', 'rating':5.0, 'cuisine':'japanese', 'id': 'japan'},
                   {'name':'Italian Restaurant', 'rating':5.0, 'cuisine':'italian', 'id': 'ital'}]
        for result in results:
            result['rating'] = result['rating']*cuisineRatings[result['cuisine']]
        return sorted(results, key=operator.itemgetter('rating'))

    def getRestaurantDetails(self, factualRestaurantID):
        # make query to Factual API based on restaurantID to get dictionary of info about this restaurant
        hardcodedRestaurantInfo = {'name': 'Kirshner\'s Cupcakes', 'address': '557 Mayfield Ave, Stanford, CA 94305', 'price':'$$$'}
        return hardcodedRestaurantInfo
