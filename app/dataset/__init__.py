from app.dataset.routes import dataset_bp

def init_dataset(app):
    app.register_blueprint(
        dataset_bp,
        url_prefix="/api/datasets"
    )