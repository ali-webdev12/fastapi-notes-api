import jwt
import os
from fastapi import HTTPException, Header
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def create_token(username : str, id : int) -> str:
    time_now = datetime.now(timezone.utc)
    payload : dict = {
        "sub" : username,
        "user_id" : id,
        "iat" : time_now,
        "exp" : time_now + timedelta(minutes=30),
        }
    
    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")

def verifi_token(token_req : str) -> dict:
    parts = token_req.split(" ")
    
    if len(parts) !=2 or parts[0].lower() != "bearer" or not parts[1]:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    clean_token = parts[1]

    try:
        payload : dict = jwt.decode(jwt=clean_token, key=SECRET_KEY, algorithms=["HS256"])
        username :str = payload.get("sub")
        user_id :int = payload.get("user_id")
        if not username or not user_id: 
            raise HTTPException(status_code=401)
        
        return {"id" : int(user_id), "username" : username}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401)

def get_current_user(authorization : str | None = Header(default=None)) -> dict:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    current_user :dict = verifi_token(authorization)
    return current_user