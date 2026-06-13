from flask import request, jsonify
from app.dataset.services import DatasetService


@dataset_bp.route("/stats", methods=["POST"])
def stats():

    # 1. get path from request body
    path = request.json.get("path")

    # 2. validate input
    if not path:
        return jsonify({"error": "Path is required"}), 400

    # 3. compute stats
    data = DatasetService.stats(path)

    return jsonify(data)