# execute fdap

if __name__ == "__main__":
    import fdap
    from fdap.app.autopost import service
    from fdap.app.autopost.autopost import AutoPost

    serviceClass = AutoPost
    # fdap.app('실행할 서비스 객체').run('실행할 메서드')
    fdap.app(service()).run('auto')
