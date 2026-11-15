from fastapi import APIRouter , Depends ,HTTPException , status
from typing import List
from sqlalchemy.orm import Session

from app.api.endpoints.deps import get_db
from app import models
from app.schema.author import Author ,AuthorCreate , AuthorUpdate


router = APIRouter()
@router.get("/" , response_model=List[Author])
def list_authors(
    skip : int =0 , limit : int  = 100 ,
    db: Session =Depends(get_db)
):
    """
    Get list authors, paginate , sample , use skip/limit
    """
    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return authors

@router.get("/{author_id}" ,response_model=Author)
def get_author(
    Author_id : int,
    db: Session = Depends(get_db)
):
    """
    Get Author detail according id 
    """
    author = db.query(models.Author).filter(models.Author.id == Author_id).first()
    if not Author : 
        raise HTTPException (
            status_code  = status.HTTP_404_NOT_FOUND,
            detail = "Author not found",
        )
    return author

@router.post("/" ,response_model=Author , status_code = status.HTTP_201_CREATED)
def create_Author(
    Author_in : AuthorCreate,
    db: Session = Depends(get_db)
):
    """
    Create new Author and check unique name
    """
    existing = db.query(models.Author).filter(models.Author.name == Author_in.name ).first()
    if existing :
        raise HTTPException (
                    status_code  = status.HTTP_400_BAD_REQUEST,
                    detail = "Author with this name already exist",
                )
    Author = models.Author(name = Author_in.name , bio = Author_in.bio )
    db.add(Author)
    db.commit()
    db.refresh(Author)
    return Author

@router.put("/{author_id}" ,response_model=Author )
def update_Author(
    Author_id : int,
    Author_up : AuthorUpdate,
    db: Session = Depends(get_db)
):
    """
    Update Author
    """
    Author = db.query(models.Author).filter(models.Author.id == Author_id ).first()

    if not Author : 
            raise HTTPException (
                status_code  = status.HTTP_404_NOT_FOUND,
                detail = "Author not found",
            )

    if Author_up.name is not None and Author_up.name != Author.name:
        existing = db.query(models.Author).filter(models.Author.name == Author_up.name ).first()
        if existing :
            raise HTTPException (
                    status_code  = status.HTTP_400_BAD_REQUEST,
                    detail = "Another Author with this name already exist",
                )
        Author.name = Author_up.name

    if Author_up.bio is not None :
            Author.bio = Author_up.bio
    db.add(Author)
    db.commit()
    db.refresh(Author)
    return Author


@router.delete("/{author_id}" ,status_code=status.HTTP_204_NO_CONTENT)
def update_Author(
    Author_id : int,
    db: Session = Depends(get_db)
):
    """
    Update Author
    """
    Author = db.query(models.Author).filter(models.Author.id == Author_id ).first()

    if not Author : 
            raise HTTPException (
                status_code  = status.HTTP_404_NOT_FOUND,
                detail = "Author not found",
            )
    db.delete(Author)
    db.commit()
