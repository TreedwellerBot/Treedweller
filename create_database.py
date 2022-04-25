import sqlite3

# connect to database and create cursor
con = sqlite3.connect('treedweller.db')
cur = con.cursor()

# create Member Table
cur.execute('''CREATE TABLE members (
                user_id INTEGER NOT NULL PRIMARY KEY, 
                sponsor INTEGER
                );''')

# create invites table
cur.execute('''CREATE TABLE invites (
                code TEXT NOT NULL PRIMARY KEY,
                user_id INTEGER,
                date_created INTEGER,
                FOREIGN KEY (user_id) REFERENCES members (user_id)
                );''')

# create ratings table
cur.execute('''CREATE TABLE ratings (
                rated_id INTEGER,
                user_id INTEGER,
                rating INTEGER,
                FOREIGN KEY (rated_id) REFERENCES members (user_id),
                FOREIGN KEY (user_id) REFERENCES members (user_id),
                PRIMARY KEY (rated_id)
                );''')
