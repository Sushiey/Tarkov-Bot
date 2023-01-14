import sqlite3

#greets the user
def Greeting(botname):
    print(botname + "Hey there, what would you like to be known as?")
    username = input("User: ")
    print(botname + "Welcome " + username + " nice to meet you, what can i help with?")

    return username

#checks for keywords in given message
def WordChecker(userMessage):
    #different lists of keywords
    commands = ["price", "info", "stats"]
    polite = ["thank you", "thanks", "cheers"]
    farewell = ["goodbye", "bye", "see you later", "adios", "ciao"]

    #checks if the message is empty
    if userMessage.split() == []:
        botResponse = "empty"
    else:
        #checks for keywords in the message from the command list
        for commandWord in commands:
            if commandWord in userMessage:
                return commandWord
        #checks for keywords in the message from the polite list
        for politeWord in polite:
            if politeWord in userMessage:
                return "polite"
        #checks for keywords in the message from the farewell list
        for farewellWord in farewell:
            if farewellWord in userMessage:
                return "goodbye"
        botResponse = "no word"
    return botResponse

#pulls list of details from SQL table
def GetDetailList(filename, keyword):
    detailList = []

    #connects to the given file
    connection = sqlite3.connect(filename)
    
    #creates a cursor and executes SQL command and select all of the data inside the table
    cursor = connection.cursor()
    filedata = cursor.execute("SELECT " + keyword + " FROM Items ORDER BY " + keyword)
    content = filedata.fetchall()

    #loops through and prints each row
    for i in range(len(content)):
        detailList.append(content[i][0])

    #closes the connection to the file
    connection.commit()
    connection.close()

    return detailList

#gets specific detail from SQL table
def GetDetail(filename, keyword, targetValue, searchValue):
    #connects to the given file
    connection = sqlite3.connect(filename)
    
    #creates a cursor and executes SQL command and select all of the data inside the table
    cursor = connection.cursor()
    filedata = cursor.execute("SELECT " + keyword + " FROM Items WHERE " + targetValue + " = '" + searchValue + "'")
    detail = filedata.fetchall()[0][0]

    #closes the connection to the file
    connection.commit()
    connection.close()

    return detail

#handles price response
def price(userMessage):
    itemList = GetDetailList(filename, "Name")

    #checks for a match between the words in the message and the available items in the database
    for item in itemList:
        if item.lower() in userMessage.lower():
            itemPrice = str(GetDetail(filename, "Price", "Name", item))
            return ("the price of the " + item + " according to my scav sources is " + itemPrice)
    return ("im sorry my friend but i couldnt find the item you were looking for")

#handles info response
def info(userMessage):
    itemList = GetDetailList(filename, "Name")

    #checks for a match between the words in the message and the available items in the database
    for item in itemList:
        if item.lower() in userMessage.lower():
            itemInfo = GetDetail(filename, "Info", "Name", item)
            return ("the information for the " + item + " according to my scav sources is " + itemInfo)
    return ("im sorry my friend but i couldnt find the information about what you were looking for")

#handles stats response
def stats(userMessage):
    itemList = GetDetailList(filename, "Name")

    #checks for a match between the words in the message and the available items in the database
    for item in itemList:
        if item.lower() in userMessage.lower():
            itemStats = GetDetail(filename, "Stats", "Name", item)
            return ("the stats for the " + item + " according to my scav sources is " + itemStats)
    return ("im sorry my friend but i couldnt find the statistics you were looking for")


#predefines some variables used throughout the program
activeCheck = True
filename = "items.db"
botname = "TarkyBot" 
username = Greeting(botname + ": ")

#loop keeps bot active
while activeCheck:
    #formats the start of the messages
    userMessage = str(input(username + ": ")).lower()
    botResponse = botname + ": "

    #checks for something to do using the given message
    procedure = WordChecker(userMessage)

    #decides what to do based on the returned keyword
    if procedure == "empty":
        botResponse += "speak up i cant hear you"
    elif procedure == "polite":
        botResponse += "you are very welcome :)"
    elif procedure == "goodbye":
        botResponse += "Thank you for the chat, hope i was some help to you. See you later " + username
        activeCheck = False
    elif procedure == "no word":
        botResponse += "do nothing"
    else:
        botResponse += eval(procedure + "(userMessage)")
    
    print(botResponse)