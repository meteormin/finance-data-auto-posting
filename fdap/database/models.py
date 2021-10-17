from database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Posts(Base):
    _tablename_ = 'posts'
    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime)
