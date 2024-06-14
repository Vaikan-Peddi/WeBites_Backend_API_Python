from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

import models, schemas, crud, db, security

router = APIRouter()

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(db.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already used')
    
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already used')
    
    db_user = crud.get_user_by_mobile(db, mobile=user.mobile)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Mobile already used')
    
    return crud.create_user(db=db, user=user)

@router.post('/signin', response_model=schemas.Token)
def signin(user_data: schemas.Signin, db: Session = Depends(db.get_db)):
    username = user_data.username
    password = user_data.password

    user = crud.get_user_by_username(db=db, username=username)
    if not user or not security.verify_password(password, user.hashed_pwd):
        raise HTTPException(status_code=400, detail="username or password incorrect.")
    
    access_token = security.create_access_token(data={"sub": user.username})
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=f"{access_token}", httponly=True, max_age=30*24*60*60)
    return response

# @router.post('/signin')
# async def signin(user_data: schemas.Signin, db: Session = Depends(db.get_db)):
#     data = user_data
#     print(data.username)
#     # username = data.get("username")
#     # password = data.get("password")

#     # user = crud.get_user_by_username(db=db, username=username)
#     # if not user or not security.verify_password(password, user.hashed_pwd):
#     #     raise HTTPException(status_code=400, detail="username or password incorrect.")
    
#     # access_token = security.create_access_token(data={"sub": user.username})
#     # response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
#     # response.set_cookie(key="access_token", value=f"{access_token}", httponly=True, max_age=30*24*60*60)
#     # return response
#     return {"msg": "hello"}

#TODO: Implement proper error handling 
@router.post('/signout')
def signout(request: Request):
    # response = JSONResponse(content={"message": "Successfully signed out"})
    # response.delete_cookie(key="access_token")
    # return response

    cookies = request.cookies.get("access_token")
    if cookies:
        response = JSONResponse(content={'message':"Signed out"})
        response.delete_cookie(key="access_token")
        return response
    else:
        response = JSONResponse(content={
            'message': 'user not signed in to signout'
        }, status_code=status.HTTP_401_UNAUTHORIZED)
        return response