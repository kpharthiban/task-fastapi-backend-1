from pydantic import BaseModel

class DBItemBase(BaseModel):
    name: str
    description: str
    is_complete: bool = False
    date: str

class DBItem(DBItemBase):
    id: int

    class Config:
        from_attributes = True