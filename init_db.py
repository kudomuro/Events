import sqlite3

connection = sqlite3.connect('./data/database.db')

with open('./data/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO events (id_day, time, tz, lead, theme, actors, enable) VALUES (1, '11:00', 'УРАЛ', 'lead1', 'theme1', 'actors1', 1)")

cur.execute("INSERT INTO events (id_day, time, tz, lead, theme, actors, enable) VALUES (5, '10:00', 'УРАЛ', 'lead2', 'theme2', 'actors2', 0)")

cur.execute("INSERT INTO days (id, day) VALUES (0, 'запланировано')")
cur.execute("INSERT INTO days (id, day) VALUES (1, 'пн')")
cur.execute("INSERT INTO days (id, day) VALUES (2, 'вт')")
cur.execute("INSERT INTO days (id, day) VALUES (3, 'ср')")
cur.execute("INSERT INTO days (id, day) VALUES (4, 'чт')")
cur.execute("INSERT INTO days (id, day) VALUES (5, 'пт')")
cur.execute("INSERT INTO days (id, day) VALUES (6, 'сб')")

connection.commit()
connection.close()