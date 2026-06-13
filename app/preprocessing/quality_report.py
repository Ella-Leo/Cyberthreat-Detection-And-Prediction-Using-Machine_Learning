class DataQualityReport:

    def generate(self, df):

        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": df.duplicated().sum(),
            "data_types": df.dtypes.astype(str).to_dict()
        }