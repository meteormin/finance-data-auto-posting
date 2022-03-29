# Resolve dependency injection
# use: from fdap.app.kiwoom import KiwoomService

def service():
    from fdap.app.kiwoom.kiwoom_service import KiwoomService
    from fdap.config.config import Config

    return KiwoomService(Config.KOAPY['account']['id'], Config.KOAPY['account']['password'])

