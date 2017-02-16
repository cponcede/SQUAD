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

    def searchForRestaurants(self, zipCode, maxDistanceMiles, pricePrefs, cuisineRatings):
        client = self.getClient()
        locationString = zipCode + ', US'
        maxDistanceMeters = str(maxDistanceMiles*1609.34)
        categoryString = ""
        for cuisineId in cuisineRatings.keys():
            categoryString = categoryString + cuisineId + ','
        categoryString = categoryString[:-1]
        searchResults = client.venues.explore(
            params={'near':locationString, 'radius':maxDistanceMeters, 'categoryId':categoryString, 'price':pricePrefs})
        finalResults = []
        for item in searchResults['groups']:
            for recommendation in item['items']:
                venueInfo = {}
                venueInfo['name'] = recommendation['venue'].get('name', 'No name available')
                venueInfo['rating'] = recommendation['venue'].get('rating', 'No rating available')
                venueInfo['address'] = ' '.join(recommendation['venue']['location'].get('formattedAddress', ['No address available']))
                venueInfo['id'] = recommendation['venue']['id']
                venueInfo['categories'] = [{'name':category['name'], 'id':category['id']} for category in recommendation['venue'].get('categories', [])]
                if 'price' not in recommendation['venue'].keys():
                    venueInfo['price'] = 'No price available'
                else:
                    venueInfo['price'] = recommendation['venue']['price']['tier']
                venueInfo['url'] = recommendation['venue'].get('url', 'No URL available.')
                venueInfo['ourRating'] = recommendation['venue'].get('rating', 0) * cuisineRatings.get(venueInfo['categories'][0]['id'], [0, 0])[1]
                finalResults.append(venueInfo)
        return sorted(finalResults, reverse=True, key=lambda item : item['ourRating'])

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
