# Resolve dependency injection
# use: from fdap.app.refine import Refine

def service():
    from fdap.app.refine.refine import Refine
    return Refine()

