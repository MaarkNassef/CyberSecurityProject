import sqlite3

def get_all_books():
    connect = sqlite3.connect('Database.db')
    cur=connect.cursor()
    cur.execute("select * from Books")
    return cur.fetchall()

def insert_user(name: str, email: str, password: str) -> bool:
    try:
        connect = sqlite3.connect('Database.db')
        connect.execute("""INSERT INTO Users (Name,Email,Password) VALUES(:name, :email, :password);""",
        {'name':name, 'email':email, 'password': password})
        connect.commit()
        connect.close()
        return True
    except:
        connect.close()
        return False

def authentication(email: str, password: str) -> bool:
    connect = sqlite3.connect('Database.db')
    cursor = connect.execute("""SELECT id FROM Users WHERE email = :email AND password = :password""",
    {'email':email, 'password': password})
    return len(cursor.fetchall()) == 1

def get_book(id: int):
    connect = sqlite3.connect('Database.db')
    cur=connect.cursor()
    cur.execute(f"select * from Books WHERE book_id = {id};")
    return cur.fetchone()

def insert_comment(book_id: int, user_id: int, comment: str):
    connect = sqlite3.connect('Database.db')
    connect.execute("""INSERT INTO Comments (book_id,User_id,book_comm) VALUES(:book_id,:user_id,:comment);""",
    {'book_id':book_id, 'user_id':user_id, 'comment': comment})
    connect.commit()
    connect.close()

def get_user_id(email: str):
    conn = sqlite3.connect('Database.db')
    cur = conn.cursor()
    cur.execute("""SELECT id FROM Users WHERE Email = :email;""", {'email':email})
    rows = cur.fetchone()
    conn.close()
    return rows[0]

def get_comments(book_id: int):
    conn = sqlite3.connect('Database.db')
    cursor = conn.execute("""SELECT u.Name,c.book_comm FROM Users u, Comments c WHERE c.book_id = :book_id AND u.id = c.User_id ORDER BY c.comm_id DESC;""",
    {'book_id': book_id})
    return cursor.fetchall()

def search_book(word: str):
    conn = sqlite3.connect('Database.db')
    cur = conn.cursor() 
    cur.execute("""SELECT * FROM Books WHERE LOWER(Title) LIKE LOWER(:word) OR LOWER(Category) LIKE LOWER(:word) OR LOWER(Author) LIKE LOWER(:word);""",
    {'word': word})
    return cur.fetchall()