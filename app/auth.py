from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(db: Session = Depends(database.get.db))
