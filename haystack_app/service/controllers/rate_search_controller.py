from flask import request, jsonify
from service.models import rate_search
from service.controllers import rate_bp


@rate_bp.route("/bm", methods=["POST"])
def bm():
    data = request.get_json()
    query = data["query"]
    k = data["k"]
    return jsonify(rate_search.search_rate_bm(query=query, k=k))


@rate_bp.route("/sb", methods=["POST"])
def sb():
    data = request.get_json()
    query = data["query"]
    k = data["k"]
    return jsonify(rate_search.search_rate_sb(query=query, k=k))


@rate_bp.route("/hybrid", methods=["POST"])
def hybrid():
    data = request.get_json()
    query = data["query"]
    k = data["k"]
    return jsonify(rate_search.search_rate_hybrid(query=query, k=k))

@rate_bp.route("/ping", methods=["GET","POST"])
def ping():
    return "pong"
