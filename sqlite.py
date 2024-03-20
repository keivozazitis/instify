import sqlite3
connection = sqlite3.connect("users_data.db")
cursor = connection.cursor()

cursor.execute("INSERT INFO users VALUES ('Janeks', 'janekslohs123')")
cursor.execute("INSERT INFO users VALUES ('Emins', 'eminadators132')")
cursor.execute("INSERT INFO users VALUES ('raivis', 'raivislohs654')")

connection.commit()