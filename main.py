from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, db, auth, college, homepage

app = FastAPI()

models.Base.metadata.create_all(bind=db.engine)

app.include_router(auth.router, prefix='/auth')
app.include_router(college.router, prefix='/college')
app.include_router(homepage.router, prefix='/homepage')