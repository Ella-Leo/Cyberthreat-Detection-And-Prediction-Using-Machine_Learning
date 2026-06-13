from flask import request, jsonify
from app.dataset.services import DatasetService


@dataset_bp.route("/preview", methods=["POST"])
def preview():

    # 1. get path from request body
    path = request.json.get("path")

    # 2. validate input
    if not path:
        return jsonify({"error": "Path is required"}), 400

    # 3. get preview data
    data = DatasetService.preview(path)

    return jsonify(data)