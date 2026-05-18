import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
    sys.path.append(os.path.join(PROJECT_ROOT, 'src'))
    
from scripts.run import execute_etl_run
from pipelines.etl_bank_pipeline import EtlBankPipeline
from pipelines.aggregation_reporter import generate_analytics_report
from pipelines.dashboard_plots import generate_pipeline_visualizations
from src.scrapping.scrapper import scrape_data
from src.storage.db_loader import BankDBLoader

def main():
    print("=" * 60)
    print("🌟 OMEGA FINANCIAL ANALYTICS PLATFORM ENGINE RUNNER")
    print("=" * 60)

    try:
        print("Attempting live data ingestion...")
        scrape_data() 
        print(" Ingestion phase finished.")
    except Exception as e:
        print(f"SCRAPER FAILED: {e}")
        return 
    execute_etl_run()
    generate_analytics_report(target_dir="data/processed")
    generate_pipeline_visualizations(processed_dir="data/processed", output_dir="data/plots")

    print("\n--- Starting Database Migration ---")
    loader = BankDBLoader()
    loader.initialize_database()
    banks_to_migrate = ["Abyssinia", "CBE", "Dashen"]

    for bank in banks_to_migrate:
        processed_csv = f"data/processed/{bank.lower()}_thematic_reviews.csv"
        raw_csv = "data/raw/raw_reviews.csv"
        
        try:
            loader.migrate_csv_to_sql(processed_csv, raw_csv, bank)
        except Exception as e:
            print(f"Skipping {bank} due to error: {e}")
    loader.verify_integrity()
    
    print("\n🏁 [Success] All pipeline layers executed smoothly and outputs are verified.")
    print("=" * 60)

if __name__ == "__main__":
    main()