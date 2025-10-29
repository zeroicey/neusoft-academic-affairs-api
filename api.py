from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from database import DatabaseManager

app = FastAPI(title="Neusoft Academic Affairs API", version="0.0.1")

db_manager = DatabaseManager()

class LoginRequest(BaseModel):
    stu_num: str
    stu_pwd: str
    
class LoginResponse(BaseModel):
    success: bool
    message: str
    stu_num: Optional[str] = None
    stu_name: Optional[str] = None
    cookie: Optional[str] = None

@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    print(request.stu_num, request.stu_pwd)


    # Query database, is there a valid cookie for stu_num?
    # If valid cookie exists:
    #   try to use it to access protected resource
    #   if access is successful:
    #       return LoginResponse with success=True and cookie info
    #   else:
    #       proceed to login with stu_num and stu_pwd
    # If no valid cookie:
    #   proceed to login with stu_num and stu_pwd

    valid_cookie = db_manager.get_valid_cookie(request.stu_num)
    if (valid_cookie):
        # Here, you would normally verify the cookie by accessing a protected resource.
        # For simplicity, we assume the cookie is valid.
        return LoginResponse(
            success=True,
            message="Login successful with cached cookie",
            stu_num=request.stu_num,
            stu_name="Student Name",
            cookie=valid_cookie
        )

    return LoginResponse(
        success=True,
        message="Login successful",
        stu_num=request.stu_num,
        stu_name="Student Name",
        cookie="cookie_value"
    )