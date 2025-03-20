from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    hashed_password: str

class LoginResponse(BaseModel):
    username: str
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class RefreshRequest(BaseModel):
    refresh_token: str