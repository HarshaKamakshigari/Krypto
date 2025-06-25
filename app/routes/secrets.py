from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.crypto import encrypt_secret, decrypt_secret
from app.db.database import SessionLocal
from app.models.secret import Secret as SecretModel

router = APIRouter()


class Secret(BaseModel):
    key: str
    value: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/store")
def store_secret(payload: Secret, db: Session = Depends(get_db)):
    existing = db.query(SecretModel).filter(SecretModel.key == payload.key).first()
    if existing:
        raise HTTPException(status_code=400, detail="Key already exists")

    encrypted = encrypt_secret(payload.value)
    secret = SecretModel(key=payload.key, value=encrypted)
    db.add(secret)
    db.commit()
    return {"message": f"Secret stored under key: {payload.key}"}

@router.get("/retrieve/{key}")
def retrieve_secret(key: str, db: Session = Depends(get_db)):
    secret = db.query(SecretModel).filter(SecretModel.key == key).first()
    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    
    decrypted = decrypt_secret(secret.value)
    return {"key": key, "value": decrypted}
