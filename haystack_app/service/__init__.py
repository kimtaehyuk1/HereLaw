import flask


def create_app():
    app = flask.Flask(__name__)

    @app.route("/ping", methods=["POST", "GET"])
    def ping():
        return "pong"

    # 블루프린트 초기화
    init_blueprint(app)

    return app


def init_blueprint(app):
    # 불루프린트로 정의된 개별 페이지 관련 내용 로드
    from .controllers import law_search_controller, rate_search_controller

    # 컨트롤러 __init__.py 에서 선언된 객체 불러오기
    from .controllers import law_bp, rate_bp

    # 플라스크 객체에 블루 프린트 등록
    law_app = app.register_blueprint(law_bp)
    rate_app = app.register_blueprint(rate_bp)

    return law_app, rate_app
