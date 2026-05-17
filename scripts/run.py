import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from transform.sentiment_pipeline import SentimentThematicTransformer

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
    
    if not os.path.exists(source_path):
        print(f"Error: Master dataset missing at absolute path: {source_path}")
        return

    print("Initializing Top-Level Discoverable Analytics Execution Run...")
    transformer = SentimentThematicTransformer()
    
    target_banks = ["CBE", "Abyssinia", "Dashen"]
    
    for bank in target_banks:
        print(f"\n🔹 Processing Pipeline Segment for: {bank}")
        print("-" * 60)
        
        master_df = pd.read_csv(source_path)
        tenant_df = master_df[master_df['bank'].str.upper() == bank.upper()].copy()
        print(f" [Extract] Successfully loaded {len(tenant_df)} rows for verification review coverage.")
        
        enriched_df = transformer.transform_dataframe(tenant_df, bank)
        

        os.makedirs(output_dir, exist_ok=True)
        safe_name = bank.lower().replace(" ", "_")
        target_csv = os.path.join(output_dir, f"{safe_name}_thematic_reviews.csv")
        enriched_df.to_csv(target_csv, index=False)
        print(f" [Load] Enriched CSV saved to target placeholder: {target_csv}")

if __name__ == "__main__":
    execute_etl_run()