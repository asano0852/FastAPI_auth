import uvicorn
import pathlib
import logging
import json

from fastapi import FastAPI,Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from auth import get_current_user, get_current_user_with_refresh_token, create_tokens, authenticate, add_user
from fastapi.responses import JSONResponse
from fastapi import Depends
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(pathname)s:%(lineno)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PATH_ROOT = str(pathlib.Path(__file__).resolve().parent)

PATH_TEMPLATES = str(pathlib.Path(__file__).resolve().parent / "templates")

templates = Jinja2Templates(directory=PATH_TEMPLATES)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    class Config:
        orm_mode = True

def error(message):
    logger.error(message, stacklevel=2)

def connect_string(protocol, username, password, host, db):
    #ローカル接続
    #return "mongodb://localhost/aig"
    #待機系接続
    return protocol + "://" + username + ":" + password + "@" + host + "/" + db

def config():
    json_open = open('config/default.json', 'r')
    json_load = json.load(json_open)

    host = json_load['host']
    path = json_load['path']
    username = json_load['username']
    password = json_load['password']
    return host, path, username, password

@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """トークン発行"""
    user = authenticate(form.username, form.password)
    return create_tokens(user.id)

@app.get("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return create_tokens(current_user.id)

@app.get('/')
def auth(request: Request):
    return templates.TemplateResponse("index.j2", context={"request": request})

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """ログイン中のユーザーを取得"""
    return current_user

@app.post("/users/create", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """ユーザー登録"""
    result = add_user(form.username, form.password)
    return JSONResponse(content={"code":0})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")