# Resolve dependency injection
# use: from fdap.app.opendart import OpenDartService

def service():
    from fdap.app.opendart.opendart_service import OpenDartService
    from fdap.config.config import Config

    config = Config.OPENDART

    return OpenDartService(config['api']['url'], config['api']['api_key'])

