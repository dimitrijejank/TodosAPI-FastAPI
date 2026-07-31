from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    email: str = Field(min_length=3)
    username: str =Field(min_length=3,max_length=55)
    first_name: str = Field(min_length=3,max_length=55)
    last_name: str = Field(min_length=3, max_length=55)
    password:str = Field(min_length=3)
    role: str = Field(min_length=3)

class Token(BaseModel):
    access_token:str
    token_type:str

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=3)