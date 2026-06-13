import os
from flask import request, jsonify

from app import db
from app.dataset.models import Dataset
from app.dataset.validators import validate_csv


@dataset_bp.route("/load", methods=["POST"])
def load_dataset():

    # 1. get path from request
    path = request.json.get("path")

    # 2. validate input
    if not path:
        return jsonify({"error": "Path is required"}), 400

    validate_csv(path)

    # 3. create dataset entry
    dataset = Dataset(
        name=os.path.basename(path),
        file_type="csv",
        file_path=path,
        size=os.path.getsize(path)
    )

    db.session.add(dataset)
    db.session.commit()

    return jsonify({
        "message": "CSV loaded successfully",
        "dataset_id": dataset.id
    })