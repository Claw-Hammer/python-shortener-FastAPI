from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from schemas import URLCreate, URLUpdate, URLResponse
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API", version="1.0.0")


@app.post("/urls", response_model=URLResponse, status_code=201)
def create_url(url_data: URLCreate, db: Session = Depends(get_db)):
    return crud.create_url(db, url_data)


@app.get("/urls", response_model=list[URLResponse])
def list_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_urls(db, skip=skip, limit=limit)


@app.get("/urls/{short_code}", response_model=URLResponse)
def get_url(short_code: str, db: Session = Depends(get_db)):
    url = crud.get_url_by_short_code(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url


@app.put("/urls/{short_code}", response_model=URLResponse)
def update_url(short_code: str, url_data: URLUpdate, db: Session = Depends(get_db)):
    url = crud.update_url(db, short_code, url_data.original_url)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url


@app.delete("/urls/{short_code}", status_code=204)
def delete_url(short_code: str, db: Session = Depends(get_db)):
    url = crud.delete_url(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return Response(status_code=204)


@app.get("/r/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    url = crud.get_url_by_short_code(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    crud.increment_clicks(db, short_code)
    return RedirectResponse(url=url.original_url)
