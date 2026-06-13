import pandas as pd
import numpy as np

class DataCleaner:

    def handle_missing(self, df):
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
        return df

    def remove_duplicates(self, df):
        return df.drop_duplicates()

    def detect_outliers_iqr(self, df):
        numeric_cols = df.select_dtypes(include=np.number).columns
        outliers = {}

        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outliers[col] = df[(df[col] < lower) | (df[col] > upper)].index.tolist()

        return outliers

    def normalize(self, df):
        numeric_cols = df.select_dtypes(include=np.number).columns
        df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (
            df[numeric_cols].max() - df[numeric_cols].min()
        )
        return df

    def standardize(self, df):
        numeric_cols = df.select_dtypes(include=np.number).columns
        df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
        return df