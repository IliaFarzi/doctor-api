from fastapi import FastAPI, HTTPException, Depends, Path, Response, status
from pydantic import BaseModel
from typing import List, Optional
import csv

# --- Pydantic models --------------------------------------

class Book(BaseModel):
    id: int
    publish_year: int
    author: str
    genre: str
    title: str

class BookIDParam(BaseModel):
    id: int = Path(..., gt=0, description="Book ID (must be > 0)")

class BookUpdate(BaseModel):
    publish_year: Optional[int]
    author: Optional[str]
    genre: Optional[str]
    title: Optional[str]

# --- App initialization -----------------------------------

app = FastAPI(title="Book Library API", version="1.0")

books: List[Book] = []

@app.on_event("startup")
def load_books():
    global books
    try:
        with open("books.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            books.clear()
            books.extend([
                Book(
                    id=int(r["id"]),
                    publish_year=int(r["publish_year"]),
                    author=r["author"],
                    genre=r["genre"],
                    title=r["title"],
                )
                for r in reader
            ])
    except FileNotFoundError:
        print("⚠️ books.csv not found. Starting with an empty list.")

# --- Routes -----------------------------------------------

@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.get("/books/{id}", response_model=Book)
def get_book_by_id(params: BookIDParam = Depends()):
    for b in books:
        if b.id == params.id:
            return b
    raise HTTPException(status_code=404, detail=f"Book with id={params.id} not found")

@app.put("/books/{id}", response_model=Book)
def update_book(
    params: BookIDParam = Depends(),
    update: BookUpdate = Depends()
):
    for idx, b in enumerate(books):
        if b.id == params.id:
            updated = b.copy(update=update.dict(exclude_unset=True))
            books[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail=f"Book with id={params.id} not found")

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(params: BookIDParam = Depends()):
    for idx, b in enumerate(books):
        if b.id == params.id:
            books.pop(idx)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Book with id={params.id} not found")
