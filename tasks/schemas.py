from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreateSchema(BaseModel):
    title : str = Field(..., max_length=50,description="this title description")
    description : Optional[str] = Field(default=None, max_length=500, description="this is description description")
    is_complete : bool = Field(default=False, description="this is tasks status")

class TaskUpdateSchema(BaseModel):
    title : str | None = Field(default=None, max_length=50,description="this title description")
    description : str | None = Field(default=None, max_length=500, description="this is description description")
    is_complete  : bool | None = Field(default=None, description="this is tasks status")

class TaskResponse(BaseModel):
    id : int 
    title : str 
    description : str | None
    is_complete : bool
    user_id : int
    created_date : datetime


