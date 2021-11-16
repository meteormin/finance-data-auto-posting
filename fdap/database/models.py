from fdap.database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, Boolean, ForeignKey


class Posts(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True)
    post_subject = Column(String(255), nullable=False)
    post_contents = Column(Text, nullable=False)
    post_category = Column(String(255), nullable=True)
    post_tags = Column(String(255), nullable=True)
    post_sector = Column(String(3), nullable=False)
    post_year = Column(String(4), nullable=False)
    report_code = Column(String(10), nullable=False)
    is_success = Column(Boolean, nullable=False, default=False)
    post_url = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return f'<Posts(post_id={self.post_id}, post_subject={self.post_subject}, post_sector={self.post_sector}, ' \
               f'post_url={self.post_url}, created_at={self.created_at})> '


class UploadedImage(Base):
    __tablename__ = 'uploaded_image'
    image_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=True)
    image_url = Column(String(255), nullable=False)
    image_path = Column(String(255), nullable=False)


class LinkedPost(Base):
    __tablename__ = 'linked_post'
    link_id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('posts.post_id'))
    child_id = Column(Integer, ForeignKey('posts.post_id'))
