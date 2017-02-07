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
        searchResults = client.venues.search(
            params={'near':locationString, 'intent':'browse', 'radius':maxDistanceMeters, 'categoryId':categoryString})
        finalResults = []
        for venue in searchResults['venues']:
            venueInfo = {}
            venueInfo['name'] = venue['name']
            venueInfo['id'] = venue['id']
            venueInfo['address'] = ' --- '.join(venue['location']['formattedAddress'])
            venueInfo['categories'] = [categoryDict['name'] for categoryDict in venue['categories']]
            finalResults.append(venueInfo)
        return finalResults

    def getRestaurantDetails(self, factualRestaurantID):
        restaurantDetails = self.getClient().venues(factualRestaurantID)['venue']
        result = {}
        result['name'] = restaurantDetails['name']
        if ('price' in restaurantDetails.keys()):
            result['price'] = restaurantDetails['price']['tier']
        else:
            result['price'] = 'No price available'
        result['categories'] = [categoryDict['name'] for categoryDict in restaurantDetails['categories']]
        result['hours'] = restaurantDetails['hours']
        result['location'] = restaurantDetails['location']['formattedAddress']
        result['rating'] = restaurantDetails['rating']
        result['menuURL'] = restaurantDetails['menu']['url']
        return result
