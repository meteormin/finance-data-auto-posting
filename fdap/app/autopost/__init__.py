# Resolve dependency injection
# use: from fdap.app.autopost import AutoPost

def service():
    from fdap.app.autopost.autopost import AutoPost
    from fdap.app.kiwoom import service as kiwoom
    from fdap.app.opendart import service as opendart
    from fdap.app.refine import service as refine
    from fdap.app.tistory import service as tistory
    from fdap.app.repositories.post_repository import PostsRepository

    return AutoPost(
        kiwoom=kiwoom(),
        opendart=opendart(),
        refine=refine(),
        tistory=tistory(),
        repo=PostsRepository()
    )
