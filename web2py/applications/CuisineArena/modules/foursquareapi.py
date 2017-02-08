#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import operator
import foursquare

class FoursquareAPI():

    def getClient(self):
        # must run sudo pip install foursquare in order for this to work
        client = foursquare.Foursquare(client_id='L1DB4SEINBUAPKNZQMLWFYSYT1RMSYHH1RSXHJ1F2IEXTLZU',
        client_secret='01WETIEETTKES04BBHJ2DKPUCXDTVNVZKSHNZPA3SQF4YI3Q')
        return client

    # TODO: Figure out how to incorporate price into this search. Currently I ignore it.
    # TODO: You can only get a restaurant's price and rating by searching that individual restaurant. 
    # I think we can work with this though if we design our UI well.
    def searchForRestaurants(self, zipCode, maxDistanceMiles, pricePrefs, cuisineRatings):
        client = self.getClient()
        locationString = zipCode + ', US'
        maxDistanceMeters = str(maxDistanceMiles*1609.34)
        # Need to create a way to associate each cuisine name with its foursquare id
        categoryString = ""
        for cuisineId in cuisineRatings.keys():
            categoryString = categoryString + cuisineId + ','
        categoryString = categoryString[:-1]
        searchResults = client.venues.explore(
            params={'near':locationString, 'radius':maxDistanceMeters, 'categoryId':categoryString})
        finalResults = []
        for item in searchResults['groups']:
            for recommendation in item['items']:
                venueInfo = {}
                venueInfo['name'] = recommendation['venue']['name']
                venueInfo['rating'] = recommendation['venue']['rating']
                venueInfo['address'] = ' '.join(recommendation['venue']['location']['formattedAddress'])
                venueInfo['id'] = recommendation['venue']['id']
                venueInfo['categories'] = [{'name':category['name'], 'id':category['id']} for category in recommendation['venue']['categories']]
                if 'price' not in recommendation['venue'].keys():
                    venueInfo['price'] = 'No price available'
                else:
                    venueInfo['price'] = recommendation['venue']['price']['tier']
                venueInfo['url'] = recommendation['venue'].get('url', 'No URL available.')
                finalResults.append(venueInfo)
        return sorted(finalResults, key=lambda item : item['rating']*cuisineRatings[item['categories'][0]['id']])

    def getRestaurantDetails(self, factualRestaurantID):
        restaurantDetails = self.getClient().venues(factualRestaurantID)['venue']
        result = {}
        result['name'] = restaurantDetails['name']
        if ('price' in restaurantDetails.keys()):
            result['price'] = restaurantDetails['price']['tier']
        else:
            result['price'] = 'No price available'
        result['categories'] = [categoryDict['name'] for categoryDict in restaurantDetails['categories']]
        result['hours'] = restaurantDetails.get('hours', 'No hours available')
        result['location'] = restaurantDetails['location']['formattedAddress']
        result['rating'] = restaurantDetails['rating']
        if 'menu' not in restaurantDetails:
            result['menuURL'] = 'No menu available'
        else:
            result['menuURL'] = restaurantDetails['menu']['url']
        return result
