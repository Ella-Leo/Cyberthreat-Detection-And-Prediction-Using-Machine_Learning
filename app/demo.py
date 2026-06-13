import pandas as pd
from service import PreprocessingService

service = PreprocessingService()

df = pd.read_csv(r'C:\Users\Admin\Desktop\ESUNGES B.Tech Project\cybersecurity_intrusion_data.csv')

cleaned, pipeline_report, quality_report = service.process_dataframe(df)

print("CLEANED DATA:")
print(cleaned.head())

print("\nPIPELINE REPORT:")
print(pipeline_report)

print("\nQUALITY REPORT:")
print(quality_report)