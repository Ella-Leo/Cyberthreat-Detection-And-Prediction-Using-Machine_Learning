from flask import Blueprint, request, jsonify
import os

from app import db
from app.dataset.models import Dataset, DatasetVersion
from app.dataset.services import DatasetService
from app.dataset.validators import validate_csv

dataset_bp = Blueprint("dataset", __name__)


# LOAD DATASET
@dataset_bp.route("/load", methods=["POST"])
def load_dataset():

    path = request.json.get("path")

    if not path:
        return jsonify({"error": "Path is required"}), 400

    validate_csv(path)

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


# PREVIEW DATASET
@dataset_bp.route("/preview", methods=["POST"])
def preview():

    path = request.json.get("path")

    if not path:
        return jsonify({"error": "Path is required"}), 400

    data = DatasetService.preview(path)

    return jsonify(data)


# DATASET STATISTICS
@dataset_bp.route("/stats", methods=["POST"])
def stats():

    path = request.json.get("path")

    if not path:
        return jsonify({"error": "Path is required"}), 400

    data = DatasetService.stats(path)

    return jsonify(data)


# DATASET VERSIONING
@dataset_bp.route("/version", methods=["POST"])
def create_version():

    path = request.json.get("path")

    if not path:
        return jsonify({"error": "Path is required"}), 400

    validate_csv(path)

    dataset = Dataset(
        name=os.path.basename(path),
        file_type="csv",
        file_path=path,
        size=os.path.getsize(path)
    )

    db.session.add(dataset)
    db.session.commit()

    new_version = DatasetVersion(
        dataset_id=dataset.id,
        version_number=1,
        file_path=path
    )

    db.session.add(new_version)
    db.session.commit()

    return jsonify({
        "message": "CSV version created",
        "dataset_id": dataset.id,
        "version": 1
    })