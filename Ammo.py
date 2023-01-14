import sqlite3
from os import path
from urllib.request import urlopen

#creates a file and database for the given filename
def CreateDatabase (filename):
    #checks if file already exists
    if not path.exists(filename):
        #creates connection to the file
        connection = sqlite3.connect(filename)

        #creates cursor and executes SQL command to create the Ammo table inside the file
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Ammo (Name TEXT,
        Damage INTEGER,
        Penetration INTEGER, 
        ArmourDamageChance INTEGER,
        AccuracyChange INTEGER,
        RecoilChange INTEGER,
        FragmentChance TEXT,
        RicochetChance TEXT,
        LightBleedChance INTEGER,
        HeavyBleedChance INTEGER,
        Velocity INTEGER,
        SpecialEffects TEXT)""")

        #closes the connection to the file
        connection.commit()
        connection.close()

#displays all the data in the database for the given file
def DisplayDatabase (filename):
    #connects to the given file
    connection = sqlite3.connect(filename)
    
    #creates a cursor and executes SQL command and select all of the data inside the table
    cursor = connection.cursor()
    filedata = cursor.execute("SELECT * FROM Ammo ORDER BY Name")
    content = filedata.fetchall()

    #loops through and prints each row
    for i in range(len(content)):
        print(content[i])

    #closes the connection to the file
    connection.commit()
    connection.close()    

#adds a row to the database given the file, name of the ammol and list of all the relevant data
def AddRow(filename, ammoName, ammoData):
    #connects to the given file
    connection = sqlite3.connect(filename)

    #creates a cursor and executes SQL command to insert the given data into the table as a new row
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Ammo VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
    (ammoName, ammoData[0], ammoData[1], ammoData[2], ammoData[3], ammoData[4], 
    ammoData[5], ammoData[6], ammoData[7], ammoData[8], ammoData[9], ammoData[10]))

    #closes the connection to the file
    connection.commit()
    connection.close()

#Selects data cell for the given ammo name 
def SelectCell(filename, chosenCol, sortVal):
    #connects to the given file
    connection = sqlite3.connect(filename)

    #creates a cursor and executes SQL command to select the chosen data for a given ammo name
    cursor = connection.cursor()
    filedata = cursor.execute("SELECT " + chosenCol + " FROM Ammo WHERE Name = ('" + sortVal + "')")
    data = filedata.fetchall()[0][0]

    #closes the connection to the file
    connection.commit()
    connection.close() 

    return data

#Selects column and orders it by the given input
def SelectColumn(filename, chosenCol, orderCol):
    #connects to the given file
    connection = sqlite3.connect(filename)

    #creates a cursor and executes SQL command to select all the data in a chosen column ordered by another given column
    cursor = connection.cursor()
    filedata = cursor.execute("SELECT Name, " + chosenCol + " FROM Ammo ORDER BY " + orderCol + " DESC")
    content = filedata.fetchall()
    
    #displays the desired column
    for i in range(len(content)):
        print(content[i])

    #closes the connection to the file
    connection.commit()
    connection.close() 



#returns the html of the table for the given url
def GetWebData(ammoType):
    ammoType = ammoType.replace(" ", "_")
    #uses the ammo type to generate a url
    url = "https://escapefromtarkov.fandom.com/wiki/" + ammoType
    webPage = urlopen(url)

    #reads the webpage and returns it as html
    htmlBytes = webPage.read()
    html = htmlBytes.decode("utf-8")

    #finds the index for the start and end of the html for the ammo table
    startIndex = html.find("<tbody>")
    endIndex = html.find("</tbody>")

    #extracts and returns the html for just the table
    webData = html[startIndex:endIndex]
    return webData

#finds the name of the ammo in the given html text
def ExtractName(htmlRow):
    #finds title within the given html
    nameStart = htmlRow.find("title") + len("title=")
    ammoName = htmlRow[nameStart:]

    #gets rid of all the unwanted parts of the title
    splitRow = ammoName.split(">")
    ammoName = splitRow[0].replace('"', "")
    ammoName = TidyUp(ammoName)

    #returns the ammo name
    return ammoName

#finds all the data for the given html row in the table
def ExtractDetails(htmlRow):
    #splits each row by the columns
    rowData = htmlRow.split("<td")
    ammoDetails = []

    #loops through each cell in the row and appends it to the end of the ammoDetails list
    for i in range(1, 12):
        data = rowData[i]
        if "data-sort" in data:
            data = data.split(">")[1][0]

        ammoDetails.append(TidyUp(data))

    #returns the list of details found for the given row
    return ammoDetails
  
#gets rid of all the unnecessary text around the desired data
def TidyUp(string):
    string = string.replace("&quot;", '"')
    string = string.replace("</td", "")
    string = string.replace("\n", "")
    string = string.replace('<font color="red">', "")
    string = string.replace('<font color="green">', "")
    string = string.replace("</font>", "")
    string = string.replace("<br /", " ")
    string = string.replace(">", "")
    if "Overpressure" in string:
        string = "Overpressure"
    if string == "":
        string = 0
    
    return string


filename = "ammoTable.db"
CreateDatabase(filename)

#list of all the ammo types that need web scraping
ammoTypes = ["7.62x25mm Tokarev", "9x18mm Makarov", "9x19mm Parabellum", "9x21mm Gyurza", ".45 ACP",
"4.6x30mm HK", "5.7x28mm FN",
"5.45x39mm", "5.56x45mm NATO", ".300 Blackout", "7.62x51mm NATO", "7.62x54mmR", ".338 Lapua Magnum", "9x39mm", ".366 TKM", "12.7x55mm STs-130",
"12x70mm","20x70mm","23x75mm",
"40x46 mm"]

#loops throught the list of ammo types
for i in range(len(ammoTypes) - 1):
    webData = GetWebData(ammoTypes[i])

    #splits the html by each row in the table
    splitData = webData.split("<tr>")

    #loops through each row in the table
    for i in range(3, len(splitData)):
        row = splitData[i]
        rowName = ExtractName(row)
        rowData = ExtractDetails(row)

        #AddRow(filename, rowName, rowData)

#debug - displays all the data in the database
DisplayDatabase(filename)
#debug - displays the damage for a given ammo name
print(SelectCell(filename, "Damage", "12/70 RIP"))
#debug - displays all the data in the Name column and orders it by the corresponding Damage
SelectColumn(filename, "Damage", "Damage")