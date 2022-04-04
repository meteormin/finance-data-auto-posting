from dependency_injector import containers, providers
from fdap.app.kiwoom.kiwoom_service import KiwoomService
from fdap.app.opendart.opendart_service import OpenDartService
from fdap.app.refine.refine import Refine
from fdap.database.database import db_session
from fdap.app.repositories.post_repository import PostsRepository
from fdap.app.tistory.tistory_client import TistoryClient, LoginInfo
from fdap.app.autopost.autopost import AutoPost


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # database
    database = providers.Singleton(db_session)

    # Services

    kiwoom_service = providers.Singleton(
        KiwoomService,
        _id=config.koapy.account.id,
        password=config.koapy.account.password
    )

    opendart_service = providers.Singleton(
        OpenDartService,
        url=config.opendart.api.url,
        api_key=config.opendart.api.api_key
    )

    refine = providers.Singleton(
        Refine
    )

    post_repository = providers.Singleton(
        PostsRepository,
        session=database
    )

    tistory_login_info = providers.Singleton(
        LoginInfo,
        client_id=config.tistory.api.client_id,
        client_secret=config.tistory.api.client_secret,
        redirect_uri=config.tistory.api.redirect_uri,
        response_type=config.tistory.api.response_type,
        login_id=config.tistory.kakao.id,
        login_password=config.tistory.password,
        state=config.tistory.api.state
    )

    tistory_client = providers.Singleton(
        TistoryClient,
        host=config.tistory.api.url,
        config=config.tistory
    )

    auto_post = providers.Singleton(
        AutoPost,
        kiwoom=kiwoom_service,
        opendart=opendart_service,
        refine=refine,
        tistory=tistory_client,
        repo=post_repository
    )


