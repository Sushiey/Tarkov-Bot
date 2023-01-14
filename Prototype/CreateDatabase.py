import sqlite3, os

def CreateDatabase (filename):
    #checks if file already exists
    if not os.path.exists(filename):
        #creates connection to the file
        connection = sqlite3.connect(filename)

        #creates cursor and executes SQL command to create the data table inside the file
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Items (Name TEXT,
        Price INTEGER,
        Info TEXT, 
        Stats TEXT)""")

        #closes the connection to the file
        connection.commit()
        connection.close()

def AddRow(filename, itemName, itemPrice, itemInfo, itemStats):
    #connects to the given file
    connection = sqlite3.connect(filename)

    #creates a cursor and executes SQL command to insert the given data into the table as a new row
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Items VALUES(?, ?, ?, ?)", (itemName, itemPrice, itemInfo, itemStats))

    #closes the connection to the file
    connection.commit()
    connection.close()

def DisplayDatabase (filename):
    #connects to the given file
    connection = sqlite3.connect(filename)
    
    #creates a cursor and executes SQL command and select all of the data inside the table
    cursor = connection.cursor()
    filedata = cursor.execute("SELECT * FROM Items ORDER BY Name")
    content = filedata.fetchall()

    #loops through and prints each row
    for i in range(len(content)):
        print(content[i])

    #closes the connection to the file
    connection.commit()
    connection.close()

filename = "items.db"

CreateDatabase(filename)
AddRow(filename, "AK101", 50000, "ak info", "ak stats")
AddRow(filename, ".338 Lapua", 500000, "lapua info", "lapua stats")
AddRow(filename, "M4A1", 45000, "m4 info", "m4 stats")
AddRow(filename, "MP7", 60000, "mp7 info", "mp7 stats")
AddRow(filename, "SVDS", 120000, "svd info", "svd stats")
AddRow(filename, "P90", 145000, "p90 info", "p90 stats")
AddRow(filename, "MK47 Mutant", 85000, "mk47 info", "mk47 stats")
AddRow(filename, "AR-15", 100000, "ar-15 info", "ar-15 stats")
AddRow(filename, "SR-25", 70000, "sr-25 info", "sr-25 stats")
DisplayDatabase(filename)