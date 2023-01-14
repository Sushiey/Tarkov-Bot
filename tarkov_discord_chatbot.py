import sqlite3
import discord
from discord import message
from Ammo import SelectCell
import api_market_handler
from datetime import datetime
#The imports that were needed to connect with discord and connect with the other files

client = discord.Client()
#This is to connect to the discord API

#This is a function that was made to help interpret the messages sent in discord and look for keywords that the bot would respond to by calling the correct function
def word_checker(message):
    keywords = {
        "price" :["price", "cost", "worth", "value",],
        "info": ["info", "information", "details", "Damage", "Penetration", "ArmourDamageChance", "AccuracyChange", "RecoilChange", "FragmentChance", "RicochetChance", "LightBleedChance", "HeavyBleedChance", "Velocity", "SpecialEffects"],
        "stats": ["stats", "statistics"]
    }
    #This is the dictionary of the keywords of each fucntion we wanted the discord bot to have 
    keys = keywords.keys()
    #This for loop goes through the message and compares each word to the dictionary and then returns the main name of the action requested
    for word in message.content.split():
        for key in keys:
            if str(word).lower() in str(keywords.get(key)).lower() or str(word).lower() == str(key).lower():
                return key
    return "no procedure"
    #This is to make the bot have no response to the user message

#This is another function that is used to futher interpret the messages sent in discord and look for the name of the ammo the user is looking for
def ammonamechecker(message):
    ammonames = getammolist()
    #This calls on another fucntion to get a list of all of the ammos that it needs to check the message for
    #This is a for loop that goes through the message again to look for the ammo name mentioned and then returns the name
    for word in message.split():
        for ammo in ammonames:
            if str(word).upper() in str(ammo).upper():
                return ammo

    return "no ammo"

#This is a funciton that uses SQL to access the ammoTable file that was made by Josh to get a list of all of the ammo names to be used in the previous function
def getammolist():
    #This connects it to the ammoTable file
    connection = sqlite3.connect("ammoTable.db")
    #This creates a cursor and excutes a SQL command to get the data that has been requested
    cursor = connection.cursor()
    filedata = cursor.execute("SELECT Name FROM Ammo ORDER BY Name")
    content = filedata.fetchall()
    #This closes the connection to the ammoTable file
    connection.commit()
    connection.close()
    return content

#This is a function that is used to futher interpret the messages sent in discord and look for the data the user is looking for
def ammodata(message):
    #This is a list of the values that are included in the ammoTable file
    valuesnames = ["Damage", "Penetration", "ArmourDamageChance", "AccuracyChange", "RecoilChange", "FragmentChance", "RicochetChance", "LightBleedChance", "HeavyBleedChance", "Velocity", "SpecialEffects"]
    #his is a for loop that goes through the message again to look for the value name mentioned and then returns the name
    for word in message.split():
        for value in valuesnames:
            if str(word).lower() in str(value).lower():
                return value
    return "Name"

#This is a function that allows us to know that the bot has been connected to
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client) + " @ " + datetime.now().strftime("%H:%M:%S"))

#This is a function that calls upon the word_checker function to start the interpretation of the message sent by a user
@client.event
async def on_message(message):
    #This if statment is to check if the message that has been sent is from the user or the bot so it knows to respond to the message or ignore it
    if message.author == client.user:
        return
    else:
        #This is where the word_checker function is called upon and the message interpretation is started
        procedure = word_checker(message)
    #This if statment is to take the return from the word_checker function and assess if a response is needed
    if procedure == "no procedure":
        print("No action needed")
    else:
        #This will make the funciton call form the return of the word_checker function
        await eval(procedure + "(message)")

#This is the function that is used to get the price of the item the user asked for from the Tarkov API
async def price(message):
    #This if statment is to check if the message that has been sent is from the user or the bot so it knows to respond to the message or ignore it
    if message.author == client.user:
        return
    else:
        #This if statment will take the user message and pass it through a function made by Daniel to check if the message contained an item from the Tarkov API and return true or false 
        if api_market_handler.isItemNamePresent(message.content):
            #This is the response that has been made from function made by Daniel to get the offical item name and price from the API and then send that message as a discord message from the bot
            response = "The " + api_market_handler.getItemName(str(message.content)) + " costs " + str(api_market_handler.getItemPrice(api_market_handler.getItemName(str(message.content)), "tMarket"))
            await message.channel.send(response)
        else:
            #This is the repsonse if the item is not found within the Tarkov API
            await message.channel.send("Item not found")

#This is the function that is used to get the information of the ammo that the user has requested
async def info(message):
    #This if statment is to check if the message that has been sent is from the user or the bot so it knows to respond to the message or ignore it
    if message.author == client.user:
        return
    else:
        #Here the fucntions that look for the name of the ammo and the value the user wants have the data the return assigned to variables to then be passed into a function that Josh made that gets the data from the ammoTable file
        ammoname = str(ammonamechecker(message.content)[0])
        ammovalue = str(ammodata(message.content))
        print(ammoname, ammovalue)
        if ammoname != "no ammo":
            #Here the selectCell function is calles and assigned to the data variable for it to then be sent to the discord channel that the user message was sent in
            data = SelectCell("ammoTable.db", ammovalue, ammoname)
            await message.channel.send(data)
    return

#This would have been the function that gets the stats on eneimies but we didnt get around to coding that
async def stats(message):
    #This if statment is to check if the message that has been sent is from the user or the bot so it knows to respond to the message or ignore it
    if message.author == client.user:
        return
    else:
        await message.channel.send("stats")

#This is what connects the code to the discord bot with a token that was given to us by discord via the developer portal
client.run('ODk5NDQ2MTUxNzM5MjE1OTMy.YWy4gQ.PI_BS8TljX4jD8Hb-DToge-1nA8')