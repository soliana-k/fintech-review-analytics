from pipelines.etl_bank_pipeline import EtlBankPipeline
from pipelines.aggregation_reporter import generate_analytics_report
from pipelines.dashboard_plots import generate_pipeline_visualizations

if __name__ == "__main__":
    
    pipeline_orchestrator = EtlBankPipeline()
    
    target_banks = ["CBE", "Abyssinia", "Dashen"]
    
    for bank in target_banks:
        pipeline_orchestrator.run_etl_for_bank(bank_name=bank)
        
    print("\n🎉 Data Platform Execution Completed Successfully!")
    generate_analytics_report()
    generate_pipeline_visualizations()