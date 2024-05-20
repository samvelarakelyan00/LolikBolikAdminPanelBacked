import mysql.connector

cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='lolikbolikdb')
print("OK")

mycursor = cnx.cursor()

# mycursor.execute("""CREATE TABLE users(
#    FIRST_NAME CHAR(20) NOT NULL,
#    LAST_NAME CHAR(20),
#    AGE INT);""")

mycursor.execute("""SELECT * FROM users""")

myresult = mycursor.fetchall()
print(myresult)
cnx.close()
