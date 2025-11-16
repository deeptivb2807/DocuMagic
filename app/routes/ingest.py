from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_ingest():
    return {"message": "Ingest router working"}