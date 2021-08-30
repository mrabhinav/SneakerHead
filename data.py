import sqlite3
conn = sqlite3.connect("userdata.db")
cur = conn.cursor()
print("Database Created")
# cur.execute("""CREATE TABLE userdata 
# (userid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT,
# lastname TEXT, username TEXT,
# location TEXT, email TEXT,
# password TEXT);""")
# cur.execute("DROP TABLE userdata")
print("Table Created")
print("Values Inserted")
records = cur.execute ("SELECT * FROM userdata") .fetchall()
email_data = []
for record in records:
    email_data.append(record[5])

print(email_data)
#cur.execute("INSERT INTO userdata (firstname, lastname, username,location, email, password) VALUES(?,?,?,?,?,?,?);", (firstname,lastname, username,location, email,password))
conn.commit()
conn.close()


