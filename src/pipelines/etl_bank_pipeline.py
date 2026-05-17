import os
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transform.sentiment_pipeline import SentimentThematicTransformer

class EtlBankPipeline:
    """
    Data Pipeline Orchestrator handling Extract (E) and Load (L) operations.
    Coordinates processing lifecycles for individual bank profiles.
    """
    def __init__(self, source_csv_path: str = "data/raw/raw_reviews.csv", target_dir: str = "data/processed"):
        self.source_path = source_csv_path
        self.target_dir = target_dir
        
        self.transformer = SentimentThematicTransformer()

    def extract_tenant_data(self, bank_name: str) -> pd.DataFrame:
        """EXTRACT (E): Ingests the master landing file and extracts isolated tenant data."""
        if not os.path.exists(self.source_path):
            raise FileNotFoundError(f"Landing layer master file missing at {self.source_path}")
            
        master_df = pd.read_csv(self.source_path)
        
        
        tenant_df = master_df[master_df['bank'].str.upper() == bank_name.upper()].copy()
        print(f"[Extract] Pulled {len(tenant_df)} rows for Tenant: {bank_name}")
        return tenant_df

    def load_processed_data(self, df: pd.DataFrame, bank_name: str):
        """LOAD (L): Persists the processed payload to an isolated staging layer destination."""
        os.makedirs(self.target_dir, exist_ok=True)
        safe_name = bank_name.lower().replace(" ", "_")
        destination_path = os.path.join(self.target_dir, f"{safe_name}_thematic_reviews.csv")
        
        df.to_csv(destination_path, index=False)
        print(f"[Load] Enriched asset safely loaded to: {destination_path}")

    def run_etl_for_bank(self, bank_name: str):
        """Orchestrates the individual linear ETL execution path for a single bank entity."""
        print(f"\n Starting ETL Pipeline execution for target: {bank_name}")
        print("-" * 50)
        
        
        raw_tenant_data = self.extract_tenant_data(bank_name)
        if raw_tenant_data.empty:
            print(f"Extract complete: No data found for {bank_name}. Terminating pipeline run.")
            return
            
        
        print(f"[Transform] Shipping chunk to stateless compute layer (NLP/Transformers)...")
        enriched_data = self.transformer.transform_dataframe(raw_tenant_data)
        
        # 3. LOAD
        self.load_processed_data(enriched_data, bank_name)
        print(f"✅ ETL Run Complete for {bank_name}!")
        print("-" * 50)