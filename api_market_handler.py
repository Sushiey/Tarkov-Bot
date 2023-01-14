#PYTHON STANDARD LIBRARY - https://docs.python.org/3/library/json.html - USED TO READ, WRITE JSON FILES STORING MARKET DATA FROM API
import json
#URLLIB 3.9 - THIRD PARTY LIBRARY - https://github.com/urllib3/urllib3 - USED TO CATCH AND HANDLE HTTP ERRORS/EXCEPTIONS
import urllib.error
#URLLIB 3.9 - THIRD PARTY LIBRARY - https://github.com/urllib3/urllib3 - USED TO REQUEST JSON DATA FROM API URL
from urllib.request import *

release_state = True

api_key = "x-api-key=9w3MIVAGdu84n6Db"
api_url = "https://tarkov-market.com/api/v1/"


#PYTHON DICTIONARY, FILE SCOPE, STORES MARKET DATA FROM API/OFFLINE JSON FILE BACKUP
marketData = None


#RETRIEVES MARKET DATA FROM API AS TYPE JSON FILE
#RETURNS MARKET DATA AS TYPE PYTHON DICTIONARY
def FetchOnlineMarketData():
    try:
        '''
        REFERENCE (LINE NUMBERS: 32, 33):

        ONLINE TUTORIAL  - https://www.geeksforgeeks.org/how-to-read-a-json-response-from-a-link-in-python/ - HOW TO OPEN JSON FILE FROM API
        YOUTUBE TUTORIAL - https://youtu.be/aj4L7U7alNU?t=159 - HOW TO OPEN JSON FILE AND PARSE TO PYTHON DICTIONARY
        '''

        #STORES DATA RETURNED FROM API (JSON FILE) USING "urlopen" IN "apiJsonFile"
        #LOADS & STORES JSON FILE (apiJsonFile) AS PYTHON DICTIONARY (online_marketData)
        print("NOTICE: ATTEMPTING TO CONNECT TO API. . .")
        apiJsonFile = urlopen(api_url + "items/all?&" + api_key)
        online_marketData = json.load(apiJsonFile)
        print("NOTICE: API CONNECTION SUCCESSFUL")

        SaveOnlineMarketData(online_marketData)

        print("\nRelease State = " + str(release_state) + "! API Connected, Market Data Up-To-Date\n")

        #RETURNS PYTHON DICTIONARY, TO BE STORED IN PYTHON DICTIONARY IN FILE SCOPE
        return online_marketData

    #HANDLES HTTP RELATED ERRORS, "aka. HTTP ERROR 249: TOO MANY REQUEST"
    #SPECIFIC HTTP ERRORS NOT HANDLED INDIVIDUALLY, ALL HTTP ERRORS RESULT IN SAME SOLUTION
    except urllib.error.HTTPError:
        print("WARNING! API CONNECTION FAILIURE, REVERTING TO OFFLINE DATA\n")
        return FetchOfflineMarketData()

#RETRIEVES MARKET DATA FROM SAVED JSON FILE
#RETURNS MARKET DATA AS PYTHON DICTIONARY
def FetchOfflineMarketData():
    print("Release State = " + str(release_state) + "!, API Not Connected, Market Data Outdated\n")

    #LOADS JSON FILE, RETURNS IT AS A PYTHON DICTIONARY TO BE STORED IN PYTHON DICTIONARY IN FILE SCOPE
    offlineMarketData_Json_File = open("offlineMarketData.json", encoding="utf-8")
    return json.load(offlineMarketData_Json_File)

#TAKES MARKET DATA FROM API AS TYPE PYTHON DICTIONARY
#SAVES PYTHON DICTIONARY AS JSON FILE (FOR USE WHEN API CONNECTION FAILS)
def SaveOnlineMarketData(updatedMarketData):
    try:
        '''
        REFERENCE (LINE NUMBERS: 70, 71):

        ONLINE TUTORIAL  - https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file - HOW TO SAVE PYTHON DICTIONARY AS JSON FILE
            MODIFIED CODE:
                with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        '''
        offlineMarketData_Json_File = open("offlineMarketData.json", "w", encoding="utf-8")
        json.dump(updatedMarketData, offlineMarketData_Json_File, ensure_ascii = False)
        print("NOTICE: OFFLINE MARKET DATA UPDATED & SAVED")
        offlineMarketData_Json_File.close()
    except:
        print("WARNING! FAILED TO UPDATE OFFLINE MARKET DATA")
        offlineMarketData_Json_File.close()

#ONLY REQUESTS MARKET DATA FROM API DATA IF "release_state" OF TYPE bool = True,
#PREVENTS "HTTP ERROR 249: TOO MANY REQUEST" DURING TESTING
if (release_state):
    marketData = FetchOnlineMarketData()
else:
    marketData = FetchOfflineMarketData()


#TAKES ITEM NAME AS TYPE str AND A USERS MESSAGE AS TYPE str
#RETURNS WETHER THE ITEM NAME IS IN THE USER MESSAGE AS TYPE bool
def MarketItem_In_userMessage(p_marketItemShortName, p_userMessage):
    if (p_marketItemShortName.replace("-", "").lower() in p_userMessage.replace("-", "").lower()):
        return True
    return False

#TAKES ITEM NAME AS TYPE str
#RETURNS WETHER THE ITEM TAG CORRESPONDS TO PREVALIDATED TAGS (PROGRAM ONLY HANDLES CERTAIN ITEMS) AS TYPE bool
def MarketItemTagValid(p_marketItemShortName):
    validTags = ["Weapon", "Ammo", "Armor_vests"]
    for marketItem in marketData:
        if (p_marketItemShortName == marketItem["shortName"]):
            for tag in validTags:
                if (tag in marketItem["tags"]):
                    return True
    return False


#TAKES A USERS MESSAGES AS TYPE str
#RETURNS WETHER AN ITEM NAME (STORED IN THE API DATA) IS PRESENT IN THE USERS MESSAGE AS TYPE bool 
def isItemNamePresent(p_userMessage):
    for marketItem in marketData:
        if (MarketItem_In_userMessage(marketItem["shortName"], p_userMessage)):
            if (MarketItemTagValid(marketItem["shortName"])):
                return True

    #ITEM NAME NOT PRESENT
    return False

#TAKES A USERS MESSAGE AS TYPE str
#RETURNS ITEM NAME (AS IT APPEARS IN API DATA) AS TYPE str OR bool = False
def getItemName(p_userMessage):
    for marketItem in marketData:
        if (MarketItem_In_userMessage(marketItem["shortName"], p_userMessage)):
            return marketItem["shortName"]
    
    #ITEM NAME NOT PRESENT
    return False

#TAKES ITEM NAME AS TYPE str AND MARKET TYPE("tMarket" OR "fMarket") AS TYPE str, 
#RETURNS CORRESPONDING ITEM PRICE (WITH CURRENCY SYMBOL PREFIXED) AS TYPE str OR bool = False
def getItemPrice(p_itemName, p_marketType):
    for marketItem in marketData:
        if (p_itemName == marketItem["shortName"]):
            if (p_marketType == "tMarket"):
                return marketItem["traderPriceCur"] + str(marketItem["traderPrice"])
            elif (p_marketType == "fMarket"):
                return marketItem["traderPriceCur"] + str(marketItem["avg24hPrice"])
            else:
                #MISSING/INCORRECT MARKET TYPE
                return False
    
    #ITEM PRICE NOT FOUND
    return False

#TAKES ITEM NAME AS TYPE str, 
#RETURNS CORRESPONDING ITEM TRADER NAME AS TYPE str OR bool = False
def getItemTraderName(p_itemName):
    for marketItem in marketData:
        if (marketItem["shortName"] == p_itemName):
            return marketItem["traderName"]
    
    #ITEM NAME NOT FOUND
    return False
