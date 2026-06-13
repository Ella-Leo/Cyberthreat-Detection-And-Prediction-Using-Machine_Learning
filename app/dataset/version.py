import os
from flask import request, jsonify

from app import db
from app.dataset.models import Dataset, DatasetVersion
from app.dataset.validators import validate_csv


@dataset_bp.route("/version", methods=["POST"])
def create_version():
    path = request.json.get("path")

    # 1. validate input
    if not path:
        return jsonify({"error": "Path is required"}), 400

    validate_csv(path)

    # 2. create dataset entry
    dataset = Dataset(
        name=os.path.basename(path),
        file_type="csv",
        file_path=path,
        size=os.path.getsize(path)
    )

    db.session.add(dataset)
    db.session.commit()

    # 3. calculate version number properly
    last_version = DatasetVersion.query.filter_by(
        dataset_id=dataset.id
    ).order_by(DatasetVersion.version_number.desc()).first()

    next_version = 1 if not last_version else last_version.version_number + 1

    # 4. create version
    new_version = DatasetVersion(
        dataset_id=dataset.id,
        version_number=next_version,
        file_path=path
    )

    db.session.add(new_version)
    db.session.commit()

    return jsonify({
        "message": "CSV version created",
        "dataset_id": dataset.id,
        "version": next_version
    })