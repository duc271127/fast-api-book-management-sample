from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints.endpoints import author,book,categories

app = FastAPI(
    title = "Book Management API",
    description= "Simple API to manage book , author , category and book covers",
    version= "1.0.0"
)
app.include_router(author.router , prefix = "/authors"  , tags = ["Authors"])
app.include_router(book.router , prefix = "/book"  , tags = ["Book"])
app.include_router(categories.router , prefix = "/categories"  , tags = ["Categories"])


@app.get("/")
def read_root():
    return{"message" : "book management API is running "}
