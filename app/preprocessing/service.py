import pandas as pd
from pipeline import PreprocessingPipeline
from quality_report import DataQualityReport

class PreprocessingService:

    def __init__(self):
        self.pipeline = PreprocessingPipeline()
        self.reporter = DataQualityReport()

    # OPTION A: dataframe input
    def process_dataframe(self, df, mode="standard"):
        cleaned_df, pipeline_report = self.pipeline.run(df, mode)
        quality_report = self.reporter.generate(cleaned_df)

        return cleaned_df, pipeline_report, quality_report

    # OPTION B: file input
    def process_csv(self, file_path, mode="standard"):
        df = pd.read_csv(file_path)

        return self.process_dataframe(df, mode)