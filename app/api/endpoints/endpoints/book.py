from fastapi import APIRouter
router = APIRouter()
@router.get("/")
def list_book():
    return {"message": "List author do it later" }