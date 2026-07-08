from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class Visibility(str, Enum):
    public = "public"
    private = "private"

class ModerationStatus(str, Enum):
    approved = "approved"
    rejected = "rejected"
    private = "private"
    pending = "pending"

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)

class LoginRequest(VerifyOtpRequest):
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class JournalCreate(BaseModel):
    title: str = Field(min_length=3, max_length=140)
    content: str = Field(min_length=20, max_length=20000)
    visibility: Visibility

class JournalUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=140)
    content: str | None = Field(default=None, min_length=20, max_length=20000)
    visibility: Visibility | None = None

class JournalOut(BaseModel):
    id: str
    title: str
    content: str | None = None
    summary: str | None = None
    category: str | None = None
    tags: list[str] = []
    sentiment: str | None = None
    emotion: str | None = None
    visibility: Visibility
    moderation_status: ModerationStatus
    moderation_reason: str | None = None
    author_name: str
    created_at: datetime
    updated_at: datetime

class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    top_k: int = Field(default=10, ge=1, le=20)
