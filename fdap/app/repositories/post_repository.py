from datetime import datetime
from typing import Union
from sqlalchemy.orm import scoped_session
from fdap.app.contracts.repositories import PostsRepository as Repo
from fdap.app.tistory.tistory_data import PostDto
from fdap.database.models import Posts


class PostsRepository(Repo):
    _model = None
    _session = None

    def __init__(self, model=None, db_session: scoped_session = None):
        """
        Args:
            model: 장고 사용 시, 모델
            db_session: SQLAlchemy 사용 시, db session
        """
        self._model = model
        self._session = db_session

    def all(self):
        query = self._session.query(Posts)
        return query.all()

    def create(self, data: PostDto):
        if isinstance(data, PostDto):
            entity = Posts()
            entity.post_subject = data.title
            entity.post_contents = data.content
            entity.post_sector = data.sector
            entity.post_category = data.category
            entity.post_tags = data.tag
            entity.created_at = datetime.now()

            self._session.add(entity)
            self._session.commit()

            return self.all()[-1]

    def find(self, identifier: Union[str, int]) -> Posts:
        return self._session.query(Posts).get(identifier)

    def find_by_sector(self, sector: str, year: str, q: str):
        return self._session.query(Posts).get(post_sector=sector, post_year=year, report_code=q)

    def update(self, identifier: Union[str, int], data: PostDto):
        entity = self.find(identifier)
        if entity is None:
            return None
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

    def delete(self, identifier: Union[str, int]):
        entity = self.find(identifier)
        self._session.query(entity).delete()
        self._session.commit()

        return True
