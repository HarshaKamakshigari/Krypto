from sqlalchemy import Column, String
from app.db.database import Base

class Secret(Base):
    __tablename__ = "secrets"

    key = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False)
