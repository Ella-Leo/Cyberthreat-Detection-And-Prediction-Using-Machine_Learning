from cleaner import DataCleaner

class PreprocessingPipeline:

    def __init__(self):
        self.cleaner = DataCleaner()

    def run(self, df, mode="standard"):

        report = {}

        # Missing values
        missing_before = df.isnull().sum().to_dict()
        df = self.cleaner.handle_missing(df)
        missing_after = df.isnull().sum().to_dict()

        # Duplicates
        before_dup = len(df)
        df = self.cleaner.remove_duplicates(df)
        after_dup = len(df)

        # Outliers
        outliers = self.cleaner.detect_outliers_iqr(df)

        # Scaling
        if mode == "normalize":
            df = self.cleaner.normalize(df)
        else:
            df = self.cleaner.standardize(df)

        report = {
            "missing_before": missing_before,
            "missing_after": missing_after,
            "duplicates_removed": before_dup - after_dup,
            "outliers": outliers,
            "final_shape": df.shape
        }

        return df, report