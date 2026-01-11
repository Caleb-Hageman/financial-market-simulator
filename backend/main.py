import fastapi as _fastapi
from typing import TYPE_CHECKING, List
from backend import schemas as _schemas
import sqlalchemy.orm as _orm
from backend import services as _services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fastapi.FastAPI()

@app.post("/api/user", response_model=_schemas.UserBase)
async def create_user(
    user: _schemas.UserCreate, 
    db: _orm.Session = _fastapi.Depends(_services.get_db)
    ):
    return await _services.create_user(user=user, db=db)