from database import DB
from schema import Book, User
from datetime import date
from passlib.context import CryptContext
from fastapi import UploadFile, File, Depends


def get_all_books():
    a = []
    result = DB.select(
        '''
       SELECT row_to_json(books) from books         
        '''
    )   
    for i in range(len(result)): 
        a.append(result[i][0])
    return a


def get_books():
    a = []
    result = DB.select(
        '''
        SELECT
            json_build_object(
                'id', b.id,
                'title', b.title,
                'img_url', b.img_url,
                'price', b.price,
                'rent_price', b.rent_price,
                'on_rent', b.on_rent,
                'category', (select name from category where id=b.category_id),
                'owner', (select username from users where users.id = b.owner_id)
            ) FROM books b
        ''' 
    )   
    for i in range(len(result)):
        a.append(result[i][0])

    return a
    

def get_book(id: int):
    result = DB.select_one(
        '''
            SELECT
                json_build_object(
                    'id', b.id,
                    'title', b.title,
                    'author', b.author,
                    'img_url', b.img_url,
                    'desc', b.description,
                    'lang', b.language,
                    'published', b.publish_year,
                    'pages', b.pages,
                    'price', b.price,
                    'rent_price', b.rent_price,
                    'on_rent', b.on_rent,
                    'category', (select name from category where id=b.category_id),
                    'owner', (select username from users where users.id = b.owner_id)
                ) FROM books b where id = %(id)s
            ''',
        {'id': id}
    )

    return result[0]


def category(category):
    name = DB.select(
        f"SELECT id FROM category WHERE name = '{category}'"
    )
    return name[0][0]


def add_book(book: Book = Depends(), file: UploadFile = File(...)):
    new_book = book.dict()
    file_name =  '192.168.100.5:8000/static/books/'+f'{file.filename}'
    category_id = category(new_book['category'].value)

    DB.execute(
        '''
            INSERT INTO books (title, author, img_url, description, language, category_id, publish_year, pages, rent_price, on_rent, price, owner_id) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        ''',    
        (new_book["title"], new_book["author"], file_name, new_book["description"], new_book["language"], category_id, new_book["published"], new_book["pages"], new_book["rent_price"], False, new_book["price"], new_book["owner_id"])
    )


def update_book(id: int, book: Book):
    DB.execute(
        '''
            UPDATE books SET (title, author) = (%s, %s) where id=%s
        ''',
        (book.title, book.author, id)
    )

def remove_book(id: int):
    DB.execute(
        '''
            DELETE FROM books where id=%s
        ''',
        (id,)
    )



####################### USERS ##################################

def correcter(cor):
    if int(cor) <= 9:
        cor = '0' + cor
        return cor
    else:
        return cor

def get_users():
    a = []
    result = DB.select(
        '''
       SELECT row_to_json(users) FROM users
        '''
    )   
    for i in range(len(result)): 
        a.append(result[i][0])
    return a


def get_user(id):
    a = []
    result = DB.select(
        f'''
       SELECT
            json_build_object(
                'id', u.id,
                'name', u.username, 
                'img_url', u.img_url,
                'age', u.age,
                'number', u.number,
                'email', u.email,
                'region', u.region,
                'address', u.address,
                'registered_at', u.registered_at,
                'books', array(select row_to_json(books) from books where u.id = books.owner_id)
            ) FROM users u where id = {id}
        '''
    )   

    for i in range(len(result)): 
        a.append(result[i][0])
    return a


def add_user(user: User, file: UploadFile = File(...)):

    new_user = user.dict()

    day = correcter(str(date.today().day))
    month = correcter(str(date.today().month))
    today = f'{day}.{month}.{str(date.today().year)}'

    bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')    
    hash_password = bcrypt_context.hash(user.password)
    
    file_name =  '192.168.100.5:8000/static/users/'+f'{file.filename}'
    
    DB.execute(
        '''
            INSERT INTO users (username, password, img_url, age, number, email, region, address, registered_at) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (new_user["username"], hash_password, file_name, new_user["age"], new_user["number"], new_user["email"], new_user["region"].value, new_user["address"], today)
    )
    
    print(new_user['region'].value)
