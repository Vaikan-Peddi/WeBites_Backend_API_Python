from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

import models, schemas, crud, db, security, util

router = APIRouter()


@router.get('/')
def homepage(curr_user: schemas.UserInDB = Depends(util.get_current_user)):

    return JSONResponse({
        'username': f'{curr_user.username}',
        'user_college_name': f'{curr_user.college.name}',
        'top_selling_list': ['list of top selling dish_restos'],
        'labels': 'Categories'
    })