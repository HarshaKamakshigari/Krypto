from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import secrets
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Krýpto: Secrets Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Krýpto server is live"}

app.include_router(secrets.router, prefix="/api")
