import base64, io, qrcode
from fastapi import APIRouter, HTTPException
from app.core.security import create_access_token, hash_password, new_totp_secret, provisioning_uri, verify_password, verify_totp
from app.db.mongodb import get_database
from app.models.schemas import LoginRequest, RegisterRequest, TokenResponse, VerifyOtpRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(payload: RegisterRequest):
    db = get_database(); secret = new_totp_secret()
    user = {"name": payload.name, "email": payload.email.lower(), "password_hash": hash_password(payload.password), "totp_secret": secret, "is_2fa_verified": False}
    try:
        await db.users.insert_one(user)
    except Exception as exc:
        raise HTTPException(409, "Email already registered") from exc
    img = qrcode.make(provisioning_uri(user["email"], secret)); buf = io.BytesIO(); img.save(buf, format="PNG")
    return {"email": user["email"], "secret": secret, "qr_code_data_url": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()}

@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(payload: VerifyOtpRequest):
    db = get_database(); user = await db.users.find_one({"email": payload.email.lower()})
    if not user or not verify_totp(user["totp_secret"], payload.otp): raise HTTPException(401, "Invalid OTP")
    await db.users.update_one({"_id": user["_id"]}, {"$set": {"is_2fa_verified": True}})
    return TokenResponse(access_token=create_access_token(str(user["_id"])))

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await get_database().users.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user["password_hash"]) or not verify_totp(user["totp_secret"], payload.otp):
        raise HTTPException(401, "Invalid credentials or OTP")
    return TokenResponse(access_token=create_access_token(str(user["_id"])))
