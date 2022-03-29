from datetime import datetime
from typing import Union, Dict
from sqlalchemy.orm import scoped_session
from sqlalchemy import desc
from fdap.contracts.repositories import PostsRepository as Repo
from fdap.app.tistory.tistory_data import PostDto
from fdap.database.models import Posts
from fdap.database.database import db_session, init_db


class PostsRepository(Repo):
    _model = None
    _session = None

    def __init__(self, session: scoped_session = None):
        """
        Args:
            session: SQLAlchemy 사용, db session
        """
        if session is None:
            init_db()
            session = db_session

        self._session = session

    def all(self):
        query = self._session.query(Posts)
        return query.all()

    def last(self):
        query = self._session.query(Posts)
        return query.order_by(desc(Posts.post_id)).first()

    def create(self, data: PostDto) -> int:
        if isinstance(data, PostDto):
            entity = Posts()
            entity.post_subject = data.title
            entity.post_contents = data.content
            entity.post_year = data.year
            entity.post_sector = data.sector
            entity.report_code = data.report_code
            entity.post_category = data.category
            entity.post_tags = data.tag
            entity.post_url = data.url
            entity.is_success = data.is_success
            entity.created_at = datetime.now()

            self._session.add(entity)
            self._session.commit()

            new_entity = self.all()[-1]
            return new_entity.post_id

    def find(self, identifier: Union[str, int]) -> Posts:
        return self._session.query(Posts).get(identifier)

    def find_by_attribute(self, attr: Dict[str, any]):
        return self._session.query(Posts).filter_by(**attr).all()

    def find_by_sector(self, sector: str, year: str, q: str):
        return self._session.query(Posts).filter_by(post_sector=sector, post_year=year, report_code=q).all()

    def update(self, identifier: Union[str, int], data: PostDto) -> bool:
        entity = self.find(identifier)
        if entity is None:
            return False
        else:
            entity.post_subject = data.title
            entity.post_contents = data.content
            entity.post_sector = data.sector
            entity.post_year = data.year
            entity.report_code = data.report_code
            entity.post_category = data.category
            entity.post_tags = data.tag
            self._session.add(entity)
            self._session.commit()
            return True

    def delete(self, identifier: Union[str, int]) -> bool:
        entity = self.find(identifier)
        self._session.query(entity).delete()
        self._session.commit()

        return True
