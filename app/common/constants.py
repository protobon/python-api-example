class App:
    name = "APP_NAME"
    host = "APP_HOST"
    port = "APP_PORT"


class MongoDB:
    uri = "MONGODB_URI"
    db = "MONGODB_DB"


class Redis:
    host = "REDIS_HOST"
    port = "REDIS_PORT"
    password = "REDIS_PASSWORD"


class Env:
    APP = App()
    MONGODB = MongoDB()
    REDIS = Redis()
