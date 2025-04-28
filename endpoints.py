from fastapi import APIRouter, Request
import asyncio
from database import url_db
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
import hashlib

router = APIRouter()


@router.get("/")
async def root():
    """Корневой endpoint"""
    return {"message": "Use POST /url to shorten URLs"}


@router.post("/shorten")
async def shorten_url(request: Request):
    """Создает короткую ссылку на текущий сервер"""

    original_url = str(request.base_url)
    short_id = hashlib.md5(original_url.encode()).hexdigest()[:8]
    url_db[short_id] = original_url

    return {
        "short_id": short_id,
        "original_url": original_url,
        "short_url": f"{original_url}{short_id}"
    }


@router.get("/{short_id}", response_class=RedirectResponse, status_code=307)
async def redirect(short_id: str):
    """Возвращает на текущий сервер по короткой ссылке"""

    if short_id not in url_db:
        raise HTTPException(404, detail=f"URL not found. Available IDs: {list(url_db.keys())}")
    return url_db[short_id]


@router.get("/async/data")
async def async_data_request():
    """Асинхронный endpoint для получения данных"""

    await asyncio.sleep(1)

    return {
        "message": "This is async data",
        "status": "processed",
        "items": [1, 2, 3]
    }
