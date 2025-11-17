from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")