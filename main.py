# uvicorn main:app --reload --host 127.0.0.1 --port 3000
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from notes import router as notes_router
import database as DB
import auth
from pwdlib import PasswordHash



app = FastAPI()
app.include_router(notes_router)
DB.init_db()
password_hash = PasswordHash.recommended()

class UserBase(BaseModel):
    username : str
    password : str

@app.post("/register")
def register_user(input_user : UserBase):
    password = password_hash.hash(input_user.password)
    new_user = {"password" : password, "username" : input_user.username}
    if DB.add_user(new_user):
        return {"message" : "User created successfully", "user" : new_user["username"]}
    else:
        raise HTTPException(status_code=409, detail="Username already exists")

@app.post("/login")
def login_user(input_user : UserBase):
    input_username, input_password = input_user.username, input_user.password
    user_from_db : dict = DB.get_user_by_user(input_username)
    if user_from_db is None:
        raise HTTPException(status_code=401 , detail="Invalid credentials")

    is_valid_password : bool = password_hash.verify(input_password, user_from_db["password"])

    if not is_valid_password:
        raise HTTPException(status_code=401 , detail="Invalid credentials")
    
    token :str = auth.create_token(input_username, user_from_db["id"])

    return {"message" : "login successfully", "token" : f"bearer {token}" }



@app.delete("/delete/me")
def delete_my_account(current_user : dict = Depends(auth.get_current_user)):
    if not DB.delete_user_by_username(current_user["username"]):
        raise HTTPException(status_code=404)

    return {"message" : "delete successfully"}

# git add . && git commit -m "update" && git push