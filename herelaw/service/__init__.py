import flask

app = flask.Flask(__name__)


def create_app():
    init_path()
    init_db()

    return app


def init_path():
    from service import controllers


def init_db():
    pass
