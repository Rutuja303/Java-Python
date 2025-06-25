from fastapi import FastAPI, status, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List,  Optional
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import auth 


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#db_dependency = Annotated(Session, Depends(get_db))

class userlogin(BaseModel):
    username: str
    password: str

class usersignup(BaseModel):
    username: str
    password: str
    email: str

class userprofile(BaseModel):
    user_id: int
    full_name: str
    email: str
    is_active: bool = True

class user(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool = True


@app.post("/login", response_model=user)
def login(user_login: userlogin, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.username == user_login.username).first()
    if not db_user or db_user.hashed_password != user_login.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return db_user

@app.post("/signup", response_model=user)
def signup(user_signup: usersignup, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.username == user_signup.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = models.Users(
        username=user_signup.username,
        email=user_signup.email,
        hashed_password=user_signup.password,  # In a real application, hash the password
        full_name=user_signup.username  # Assuming full_name is same as username for simplicity
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.post("/profile", response_model=userprofile)
def create_profile(profile: userprofile, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.id == profile.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    new_profile = models.UserProfile(
        user_id=profile.user_id,
        full_name=profile.full_name,
        email=profile.email,
        is_active=profile.is_active
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile

@app.get("/users", response_model=List[user])
def get_users(
    name: Optional[str] = Query(None, description="Search by username"),
    db: Session = Depends(get_db)
):
    if name:
        users = db.query(models.Users).filter(models.Users.username.ilike(f"%{name}%")).all()
    else:
        users = db.query(models.Users).all()
    return users


