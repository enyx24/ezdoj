from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    token_type: str = "bearer"
    expires_in: int

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    full_name: str | None = None

class SignupResponse(BaseModel):
    message: str

