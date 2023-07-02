from flask import Blueprint

# 판례(사례) 검색 서비스
law_bp = Blueprint(
    "law_bp",
    __name__,
    url_prefix="/law",
)

# 과실비율 검색 서비스
rate_bp = Blueprint(
    "rate_bp",
    __name__,
    url_prefix="/rate",
)
