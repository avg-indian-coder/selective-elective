import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1MuSigma!'
)

# cursor object
cursorObject = dataBase.cursor()

# create the database
cursorObject.execute("CREATE DATABASE electives")

print("All done!")