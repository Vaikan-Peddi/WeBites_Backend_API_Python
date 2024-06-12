from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, crud, db, security, auth

app = FastAPI()

models.Base.metadata.create_all(bind=db.engine)

def get_current_user(request: Request, db: Session = Depends(db.get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated")
    
    payload = security.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    
    username: str = payload.get("sub")
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    
    return user

@app.get('/protected', response_model=schemas.UserResponse)
def protected(current_user: schemas.UserInDB = Depends(get_current_user)):
    return current_user

app.include_router(auth.router, prefix='/auth')