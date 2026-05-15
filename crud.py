import string
import random
from sqlalchemy.orm import Session
from models import URL
from schemas import URLCreate


def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def create_url(db: Session, url_data: URLCreate):
    short_code = generate_short_code()
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    db_url = URL(original_url=url_data.original_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_urls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(URL).offset(skip).limit(limit).all()


def get_url_by_short_code(db: Session, short_code: str):
    return db.query(URL).filter(URL.short_code == short_code).first()


def update_url(db: Session, short_code: str, original_url: str):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if db_url:
        db_url.original_url = original_url
        db.commit()
        db.refresh(db_url)
    return db_url


def delete_url(db: Session, short_code: str):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if db_url:
        db.delete(db_url)
        db.commit()
    return db_url


def increment_clicks(db: Session, short_code: str):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if db_url:
        db_url.clicks += 1
        db.commit()
        db.refresh(db_url)
    return db_url
