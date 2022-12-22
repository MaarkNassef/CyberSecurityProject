import sqlite3

def get_all_books():
    connect = sqlite3.connect('Database.db')
    cur=connect.cursor()
    cur.execute("select * from Books")
    return cur.fetchall()

def insert_user(name: str, email: str, password: str, credit, credit_tag, credit_nonce) -> bool:
    try:
        connect = sqlite3.connect('Database.db')
        connect.execute("""INSERT INTO Users (Name,Email,Password,Credit, Credit_tag, Credit_nonce) VALUES(:name, :email, :password, :credit, :credit_tag, :credit_nonce);""",
        {'name':name, 'email':email, 'password': password, 'credit':credit, 'credit_tag':credit_tag, 'credit_nonce': credit_nonce})
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

def insert_book(book_title: str, book_author:str, book_category: str, book_stars: str, book_description: str ,image_title: str,  image):
    connect = sqlite3.connect('Database.db')
    connect.execute("""INSERT INTO Books (Title,Author,Category,Stars, Description) 
                        VALUES(:book_title,:book_author,:book_category,:book_stars, :book_description);""",
    {'book_title':book_title, 'book_author':book_author, 'book_category': book_category, 'book_stars':book_stars, 'book_description':book_description})
    connect.execute("""INSERT INTO BookImage VALUES(:book_title, :image_title, :image)""",{'book_title':book_title, 'image_title':image_title ,'image':image})
    connect.commit()
    connect.close()

def get_image(book_title: str):
    conn = sqlite3.connect('Database.db')
    cursor = conn.execute("""SELECT * FROM BOOKIMAGE WHERE book_title = :book_title""",
    {'book_title': book_title})
    return cursor.fetchone()
