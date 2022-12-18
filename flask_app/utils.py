from datetime import datetime
import requests
import ast

def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")



def parseAddress(restaurant:dict):
    address = restaurant["addressCountry"] + ", " + restaurant["addressLocality"] + ", " + restaurant["addressRegion"] + ", " + restaurant["neighborhood"] + ", " + restaurant["postalCode"]

    return address


def process_query(query, allRestaurants) -> list:
    #print(type(query), query)
    
    if '{' in query:
        query = ast.literal_eval(query)

    if type(query) is not dict:
        jsonData = api_call(query)
        places = jsonData["places"]["value"]
        restaurants = []

        for place in places:
            if place["_type"] == "Restaurant":
                restaurants.append(place['name'] + ": " + parseAddress(place['address']))

        return [*set(restaurants)]

    elif type(query) is dict:
        # find best matches
        
        scores = []

        for restaurant in allRestaurants:
            totalScore = 0

            if query['romance'] == restaurant.averageRomance:
                totalScore += 1
            
            if query['occasion'] == restaurant.averageOccasion:
                totalScore += 1
            
            if query['price'] == restaurant.averagePrice:
                totalScore += 1
            
            scores.append((restaurant.restaurant_details, totalScore, restaurant.averageRecommend))
        
        scores.sort(key=lambda x: (x[1], x[2]), reverse=True)

        #print(scores)

        finalList = [x for x, _, _ in scores[:10]]

        return finalList


        '''
        'romance': attributeForm.romance.data,
        'occasion': attributeForm.occasion.data,
        'price': attributeForm.price.data,
        '''








def api_call(query) -> dict:

    url = "https://bing-entity-search.p.rapidapi.com/entities"

    addedParams = "Restaraunt"

    querystring = {"q": query + addedParams,"mkt":"en-us"}

    headers = {
        "X-BingApis-SDK": "true",
        "X-RapidAPI-Key": "773b0760d7msha5e61866e40dda6p147c4cjsnf0cbcf125558",
        "X-RapidAPI-Host": "bing-entity-search.p.rapidapi.com"
    }

    #response = requests.request("GET", url, headers=headers, params=querystring)

    #print("!!!!!!!!!!!!!query made!!!!!!!!!!!!!!")

    #return response.json()

    # testing
    return {"_type": "SearchResponse", "queryContext": {"_type": "QueryContext", "originalQuery": "Barcelona Wine Bar, Washington DC"}, "places": {"_type": "Places", "value": [{"_type": "Restaurant", "id": "https:\/\/www.bingapis.com\/api\/v7\/#Places.0", "webSearchUrl": "https:\/\/www.bing.com\/entityexplore?q=Barcelona+Wine+Bar&filters=local_ypid:%22YN873x571802624796545990%22&elv=AXXfrEiqqD9r3GuelwApulpjW6ZpR1Iuctp!uJ1OhS4bzhEua56sdYhUQ3ivPM9sHV4UTxJ!hgDLViMDPSLm8kFSaXO7elHKn3gyVldZ*srR", "name": "Barcelona Wine Bar", "url": "https:\/\/www.barcelonawinebar.com\/location\/14th-street\/?utm_source=yext&utm_medium=localsearch&utm_campaign=landing-page&utm_content=14-street", "entityPresentationInfo": {"_type": "Entities\/EntityPresentationInfo", "entityScenario": "ListItem", "entityTypeHints": ["Place", "LocalBusiness", "Restaurant"]}, "address": {"_type": "PostalAddress", "addressLocality": "Washington", "addressRegion": "DC", "postalCode": "20009", "addressCountry": "US", "neighborhood": "Logan Circle"}, "telephone": "(202) 588-5500"}, {"_type": "Restaurant", "id": "https:\/\/www.bingapis.com\/api\/v7\/#Places.1", "webSearchUrl": "https:\/\/www.bing.com\/entityexplore?q=Barcelona+Wine+Bar&filters=local_ypid:%22YN873x4865160653596904407%22&elv=AXXfrEiqqD9r3GuelwApulpjW6ZpR1Iuctp!uJ1OhS4bzhEua56sdYhUQ3ivPM9sHV4UTxJ!hgDLViMDPSLm8kFSaXO7elHKn3gyVldZ*srR", "name": "Barcelona Wine Bar", "url": "https:\/\/www.barcelonawinebar.com\/location\/cathedral-heights\/?utm_source=yext&utm_medium=localsearch&utm_campaign=landing-page&utm_content=cathedral-heights", "entityPresentationInfo": {"_type": "Entities\/EntityPresentationInfo", "entityScenario": "ListItem", "entityTypeHints": ["Place", "LocalBusiness", "Restaurant"]}, "address": {"_type": "PostalAddress", "addressLocality": "Washington", "addressRegion": "DC", "postalCode": "20016", "addressCountry": "US", "neighborhood": "Cleveland Park"}, "telephone": "(202) 800-4100"}, {"_type": "Restaurant", "id": "https:\/\/www.bingapis.com\/api\/v7\/#Places.2", "webSearchUrl": "https:\/\/www.bing.com\/entityexplore?q=Barcelona+Wine+Bar&filters=local_ypid:%22YN873x571802624796545990%22&elv=AXXfrEiqqD9r3GuelwApulpjW6ZpR1Iuctp!uJ1OhS4bzhEua56sdYhUQ3ivPM9sHV4UTxJ!hgDLViMDPSLm8kFSaXO7elHKn3gyVldZ*srR", "name": "Barcelona Wine Bar", "url": "https:\/\/www.barcelonawinebar.com\/location\/14th-street\/?utm_source=yext&utm_medium=localsearch&utm_campaign=landing-page&utm_content=14-street", "entityPresentationInfo": {"_type": "Entities\/EntityPresentationInfo", "entityScenario": "ListItem", "entityTypeHints": ["Place", "LocalBusiness", "Restaurant"]}, "address": {"_type": "PostalAddress", "addressLocality": "Washington", "addressRegion": "DC", "postalCode": "20009", "addressCountry": "US", "neighborhood": "Logan Circle"}, "telephone": "(202) 588-5500"}]}, "rankingResponse": {"_type": "Ranking\/RankingResponse", "mainline": {"_type": "Ranking\/RankingGroup", "items": [{"_type": "Ranking\/RankingItem", "answerType": "Places"}, {"_type": "Ranking\/RankingItem", "answerType": "Places", "resultIndex": 0, "value": {"_type": "Identifiable", "id": "https:\/\/www.bingapis.com\/api\/v7\/#Places.0"}}, {"_type": "Ranking\/RankingItem", "answerType": "Places", "resultIndex": 1, "value": {"_type": "Identifiable", "id": "https:\/\/www.bingapis.com\/api\/v7\/#Places.1"}}]}, "sidebar": {"_type": "Ranking\/RankingGroup", "items": [{"_type": "Ranking\/RankingItem", "answerType": "Places", "resultIndex": 2, "value": {"_type": "Identifiable", "id": "https:\/\/www.bingapis.com\/api\/v7\/#Places.2"}}]}}}



    