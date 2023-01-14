import sqlite3

def DisplayDatabase(filename):
    connection = sqlite3.connect(filename)
    mycursor = connection.cursor()

    filedata = mycursor.execute("SELECT * FROM scavbosses")
    tablecontent = filedata.fetchall()

    for i in range(len(tablecontent)):
        print(tablecontent[i])

    connection.commit()
    connection.close()

def Createtable(filename):
    cnn = sqlite3.connect(filename)
    mycursor = cnn.cursor()

    # create table
    sql_new_table = ("""CREATE TABLE scavbosses
    (Name text,
     NumberOfMinions text,
     Armour,
     Weapon TEXT,
     LootableItems TEXT)""")
    mycursor.execute(sql_new_table)

    cnn.commit()
    mycursor.close()

def AddRow(filename):
    cnn = sqlite3.connect(filename)
    mycursor = cnn.cursor()

    # create table
    #mycursor.execute("""INSERT INTO scavbosses VALUES ('Killa','0', '6b13 assult', '5.45 Rpk', 'Red Card')""")
    #mycursor.execute("""INSERT INTO scavbosses VALUES ('Glukhar','6', 'taktical tv armoured rig', 'ASh-12 12.7x55 assault rifle', 'Red Card')""")
    #mycursor.execute("""INSERT INTO scavbosses VALUES ('Sanitar','2', 'None', 'OP-SKS, VSS', 'blue key card')""")
    #mycursor.execute("""INSERT INTO scavbosses VALUES ('Shturman','2', 'None', 'AK-105 5.45x39','blue key card')""")
    #mycursor.execute("""INSERT INTO scavbosses VALUES ('Reshala','4', 'None', 'AK-101 5.56x45','Golden TT')""")


    cnn.commit()
    mycursor.close()


#Createtable("scavbosses.db")
#DisplayDatabase("scavbosses.db")
#AddRow("scavbosses.db")