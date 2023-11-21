import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1MuSigma!'
)

cur = dataBase.cursor()

# put highest num of students on the lowest floor possible
# therefore highest students get most priority
# sort EF in descending order of students
# assign first class with capacity >= students
cur.execute('''
    use electives;
''')

cur.execute('''
INSERT into website_Room values
            ('B000', 0, 50),
            ('B001', 0, 60),
            ('B002', 0, 30), 
            ('B100', 1, 20),
            ('B101', 1, 40),
            ('B102', 1, 70),
            ('B200', 2, 15),
            ('B201', 2, 20),
            ('B202', 2, 25),
            ('B300', 3, 10),
            ('B301', 3, 5),
            ('B302', 3, 20);
''')

dataBase.commit()
print("all done!!!")
cur.close()