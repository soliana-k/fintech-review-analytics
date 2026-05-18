import os
import pandas as pd
import sys
import re
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transform.sentiment_pipeline import SentimentThematicTransformer

class EtlBankPipeline:
    """
    Data Pipeline Orchestrator handling Extract (E), Clean/Filter, and Load (L) operations.
    Coordinates processing lifecycles for individual bank profiles.
    """
    def __init__(self, source_csv_path: str = "data/raw/raw_reviews.csv", target_dir: str = "data/processed"):
        self.source_path = source_csv_path
        self.target_dir = target_dir
        self.transformer = SentimentThematicTransformer()

    def _is_english_only(self, text: str) -> bool:
        """Internal helper to detect and filter non-English content."""
        if not isinstance(text, str) or text.strip() == "":
            return False
            
        if bool(re.search(r'[\u1200-\u137F]', text)):
            return False
           
        try:
            return detect(text) == 'en'
        except:
            return False

    def extract_tenant_data(self, bank_name: str) -> pd.DataFrame:
        """EXTRACT (E): Ingests master file, isolates tenant, and filters for English reviews."""
        if not os.path.exists(self.source_path):
            raise FileNotFoundError(f"Landing layer master file missing at {self.source_path}")
            
        master_df = pd.read_csv(self.source_path)
        tenant_df = master_df[master_df['bank'].str.upper() == bank_name.upper()].copy()
        initial_count = len(tenant_df)
        tenant_df = tenant_df[tenant_df['review'].apply(self._is_english_only)]
        dropped_count = initial_count - len(tenant_df)
        print(f"[Extract] Pulled {len(tenant_df)} rows for {bank_name} (Dropped {dropped_count} non-English reviews)")
        
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
            print(f"Extract complete: No valid English data found for {bank_name}. Terminating.")
            return
        
        print(f"[Transform] Shipping {len(raw_tenant_data)} reviews to NLP compute layer...")
        enriched_data = self.transformer.transform_dataframe(raw_tenant_data, bank_name)
        self.load_processed_data(enriched_data, bank_name)
        print(f"ETL Run Complete for {bank_name}!")
        print("-" * 50)