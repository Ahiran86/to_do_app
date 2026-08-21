from pydantic import BaseModel, Field, model_validator
from fastapi import HTTPException, status



class UserSignupSchema(BaseModel):
    username : str = Field(..., max_length=150)
    password : str = Field(..., max_length=150, min_length=8)
    password_confirm : str = Field(..., max_length=150, min_length=8)

    @model_validator(mode="after")
    def chek_name_password(self):
        if self.username == self.password :
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="you can't import same username and password")
        return self
   
    @model_validator(mode="after")
    def check_password(self):
        if self.password != self.password_confirm:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="passwords do not match")
        return self


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=150)
    password: str = Field(..., max_length=150, min_length=8)
