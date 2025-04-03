from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, Float

class DBItemsTable(Base):
    __tablename__ = "DBItems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    is_complete = Column(Boolean)
    date = Column(String)