from fastapi import APIRouter, UploadFile, File, Depends

import service
from schema import Book, User

IMAGEDIR = 'static/books/'
book_app = APIRouter()


@book_app.get("/books", tags=["Books"])
def get_all_books():
    return service.get_all_books()


@book_app.get("/books/{book_id}", tags=["Books"])
def get_one_book(book_id: int):
    return service.get_book(book_id)


@book_app.post("/books", tags=["Books"])
async def create_book(book: Book = Depends(), file: UploadFile = File(...)):

    BOOKDIR = 'static/books/'
    contents = await file.read()  # <-- Important!

    with open(f"{BOOKDIR}{file.filename}", "wb") as f:
        f.write(contents)
    
    return service.add_book(book, file)


@book_app.put("/books/{book_id}", tags=["Books"])
def custom_book(book_id: int, book: Book):
    return service.update_book(book_id, book)


@book_app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int):
    return service.remove_book(book_id)


####################### USERS ##################################


@book_app.get("/users", tags=["Users"])
def get_all_users():
    return service.get_users()


@book_app.get('/users/{id}', tags=["Users"])
def get_user(id: int):
    return service.get_user(id)



@book_app.post('/add_user', tags=["Users"])
async def create_user(user: User = Depends(), file: UploadFile = File(...)):
    
    USERDIR = 'static/users/'
    contents = await file.read()  # <-- Important!

    with open(f"{USERDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return service.add_user(user, file)
