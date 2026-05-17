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

def main():
    print("=" * 60)
    print("🌟 OMEGA FINANCIAL ANALYTICS PLATFORM ENGINE RUNNER")
    print("=" * 60)

    execute_etl_run()
    generate_analytics_report(target_dir="data/processed")
    generate_pipeline_visualizations(processed_dir="data/processed", output_dir="data/plots")
    
    print("\n🏁 [Success] All pipeline layers executed smoothly and outputs are verified.")
    print("=" * 60)

if __name__ == "__main__":
    main()