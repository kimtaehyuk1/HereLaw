from flask import request, jsonify
from service.models import law_search
from service.controllers import law_bp


@law_bp.route("/bm", methods=["POST"])
def bm():
    data = request.get_json()
    query = data["query"]
    k = data["k"]
    return jsonify(law_search.search_law_bm(query=query, k=k))


@law_bp.route("/sb", methods=["POST"])
def sb():
    data = request.get_json()
    query = data["query"]
    k = data["k"]
    return jsonify(law_search.search_law_sb(query=query, k=k))


@law_bp.route("/hybrid", methods=["POST"])
def hybrid():
    data = request.get_json()
    query = data["query"]
    k = data["k"]
    return jsonify(law_search.search_law_hybrid(query=query, k=k))


@law_bp.route("/ping", methods=["GET","POST"])
def ping():
    return "pong"
