from typing import TYPE_CHECKING
from backend import database as _db
from backend import models as _models
from backend import schemas as _schemas
from passlib.context import CryptContext # type: ignore

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
#############
_pwd_context = CryptContext(schemes=["argon2"], deprecated="auto",)


def _hash_password(password: str) -> str:
    return _pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)
###########
def _add_tables():
    return _db.Base.metadata.create_all(bind=_db.engine)

def get_db():
    db = _db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_user(
        user: _schemas.UserCreate, 
        db: "Session"
) -> _schemas.UserBase:
    db_user = _models.User(email=user.email, hashed_password=_hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return _schemas.UserResponse.model_validate(db_user)