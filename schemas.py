from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime


class URLCreate(BaseModel):
    original_url: str

    @field_validator("original_url")
    @classmethod
    def validate_url(cls, v):
        try:
            HttpUrl(v)
        except Exception:
            raise ValueError("Invalid URL format")
        return v


class URLUpdate(BaseModel):
    original_url: str

    @field_validator("original_url")
    @classmethod
    def validate_url(cls, v):
        try:
            HttpUrl(v)
        except Exception:
            raise ValueError("Invalid URL format")
        return v


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    created_at: datetime
    clicks: int

    class Config:
        from_attributes = True
