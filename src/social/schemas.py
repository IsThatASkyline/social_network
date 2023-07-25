from pydantic import BaseModel


class PostCreate(BaseModel):
    text: str

    class Config:
        from_attributes = True


class PostUpdate(PostCreate):
    pass


class PostRead(BaseModel):
    text: str
    owner_id: int
    likes_amount: int
    dislikes_amount: int

    class Config:
        from_attributes = True
