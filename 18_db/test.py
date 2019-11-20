import sqlite3


connection = sqlite3.connect(r'C:\sqlite\testDB.db')
cursor = connection.cursor()

for row in cursor.execute('select * from switch'):
    print(row)


