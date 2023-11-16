import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1MuSigma!'
)

cur = dataBase.cursor()

cur.execute('''
    use electives;
''')

cur.execute('''
    INSERT into website_Faculty values
               (1, "Gowri", "Srinivasa"),
               (2, "Prafullata", "Auradkar"),
               (3, "Srinivas", "KS");
''')

cur.execute('''
    INSERT into website_Elective values
               (1, "Data Analytics", 1),
               (2, "Advanced Algorithms", 1),
               (3, "IoT", 1),
               (4, "Big Data", 2),
               (5, "CNS", 2),
               (6, "Graph Theory", 2);
''')

cur.execute('''
    INSERT into website_ElectiveTeachingFaculty
               (F_id_id, E_id_id, student_no) values
               (1, 1, 0),
               (3, 1, 0),
               (3, 2, 0),
               (2, 2, 0),
               (1, 3, 0),
               (2, 4, 0),
               (3, 4, 0),
               (1, 5, 0),
               (2, 6, 0);
''')

dataBase.commit()
print("All done")
cur.close()