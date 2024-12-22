import string
import random
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import URLItem
import validators
from datetime import datetime
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()


class URLCreate(BaseModel):
    url: HttpUrl


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@app.post("/shorten")
def shorten_url(item: URLCreate, db: Session = Depends(get_db)):
    # Генерируем уникальный short_id
    for _ in range(10):
        short_id = generate_short_id()
        existing = db.query(URLItem).filter(URLItem.short_id == short_id).first()
        if not existing:
            new_item = URLItem(
                short_id=short_id, full_url=str(item.url), created_at=datetime.now()
            )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {"short_url": f"http://localhost:8000/{short_id}"}
    raise HTTPException(
        status_code=500, detail="Не удалось сгенерировать короткую ссылку"
    )


def list_all_urls(db: Session = Depends(get_db)):
    """Возвращает список всех коротких ссылок с их оригинальными адресами."""
    urls = db.query(URLItem).all()
    return [
        {
            "short_id": url.short_id,
            "full_url": url.full_url,
            "created_at": url.created_at.isoformat()
            if hasattr(url, "created_at")
            else None,
        }
        for url in urls
    ]


def health_check():
    """Проверяет состояние сервиса."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/{short_id}")
def redirect_to_full(short_id: str, db: Session = Depends(get_db)):
    if short_id == "list":
        return list_all_urls(db)
    if short_id == "health":
        return health_check()
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    if len(short_id) != 6 and not validators.url(short_id):
        raise HTTPException(status_code=400, detail="Некорректный URL")
    # Проверяем, что в базе данных хранится корректный URL
    return RedirectResponse(url=url_item.full_url)


@app.get("/")
def get_stats():
    return {"info":"Short url app сделанный Вороновым Никитой"}


@app.get("/stats/{short_id}")
def get_stats(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return {"short_id": url_item.short_id, "full_url": url_item.full_url}


@app.delete("/{short_id}")
def delete_short_url(short_id: str, db: Session = Depends(get_db)):
    """Удаляет короткую ссылку по short_id."""
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    db.delete(url_item)
    db.commit()
    return {"detail": "Короткая ссылка удалена"}


@app.put("/{short_id}")
def update_url(short_id: str, updated_url: URLCreate, db: Session = Depends(get_db)):
    """Обновляет оригинальный URL по его short_id."""
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    url_item.full_url = str(updated_url.url)
    db.commit()
    db.refresh(instance=url_item)
    return {
        "detail": "URL обновлен",
        "short_id": url_item.short_id,
        "full_url": url_item.full_url,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
