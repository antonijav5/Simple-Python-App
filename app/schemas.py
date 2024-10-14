from pydantic import BaseModel
from typing import List

class PostBase(BaseModel):
    title: str
    content: str

class CommentBase(BaseModel):
    content: str

class TagBase(BaseModel):
    tag_name: str

class UserBase(BaseModel):
    username: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True  

class PostResponse(PostBase):
    id: int
    tags: List[TagBase] = []  

    class Config:
        orm_mode = True  
