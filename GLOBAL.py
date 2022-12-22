import sqlite3

userEmail = ''

def getUserId(email):
    print(email)
    conn = sqlite3.connect('Database.db')
    cur = conn.cursor()
    query = f"SELECT id FROM Users WHERE Email = '{email}';"
    cur.execute(query)
    rows = cur.fetchone()
    conn.close()
    return rows[0]

def getEmail():
    return userEmail

def isSignedIn():
    return not(userEmail == '')
