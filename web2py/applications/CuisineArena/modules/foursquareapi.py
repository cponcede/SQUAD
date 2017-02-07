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
        # make query to Factual API based on restaurantID to get dictionary of info about this restaurant
        client = self.getClient()
        hardcodedRestaurantInfo = {'name': 'Kirshner\'s Cupcakes', 'address': '557 Mayfield Ave, Stanford, CA 94305', 'price':'$$$'}
        return hardcodedRestaurantInfo
