import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.pipelines.etl_bank_pipeline import EtlBankPipeline

def execute_etl_run():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    marker = "fintech-review-analytics"
    
    if marker in current_file_dir:
        base_part = current_file_dir.split(marker)[0]
        project_root = os.path.join(base_part, marker)
    else:
        project_root = os.path.abspath(os.path.join(current_file_dir, ".."))

    source_path = os.path.join(project_root, "data/raw/raw_reviews.csv")
    output_dir = os.path.join(project_root, "data/processed")
    
    pipeline = EtlBankPipeline(source_csv_path=source_path, target_dir=output_dir)
    
    target_banks = ["CBE", "Abyssinia", "Dashen"]
    
    for bank in target_banks:
        pipeline.run_etl_for_bank(bank)


if __name__ == "__main__":
    execute_etl_run()