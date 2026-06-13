import pandas as pd

from app.dataset.validators import validate_csv


class DatasetService:

    @staticmethod
    def load_csv(path):
        validate_csv(path)
        return pd.read_csv(path)

    @staticmethod
    def preview(path, rows=20):
        df = DatasetService.load_csv(path)
        return df.head(rows).to_dict(orient="records")

    @staticmethod
    def stats(path):
        df = DatasetService.load_csv(path)

        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list(df.columns)
        }   