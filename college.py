from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

import models, schemas, crud, db, security

router = APIRouter()

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    return user

@router.get('/list')
def college_list(offset: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    clg_list = crud.get_college_list(db=db, offset=offset, limit=limit)
    return {
        'message': f'college list with offset: {offset} and limit: {limit}',
        'college_list': clg_list
    }

@router.post('/list/{college_id}')
def select_college(college_id: int, curr_user: schemas.UserInDB = Depends(get_current_user), db: Session = Depends(db.get_db)):
    if curr_user.college_id is not None:
        return JSONResponse(content={
            'message': f'College already selected of id: {curr_user.college_id}'
        }, status_code=status.HTTP_409_CONFLICT)
    
    try: 
        db_user = db.query(models.User).filter(models.User.id == curr_user.id).first()
        db_user.college_id = college_id
        db.commit()
        return JSONResponse(content={
            'message': f'Added college: {db_user.college.name}'
        })
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    

#TODO: Add an endpoint for changing college