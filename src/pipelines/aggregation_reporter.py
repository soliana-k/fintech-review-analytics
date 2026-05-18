import os
import pandas as pd

def generate_analytics_report(target_dir: str = "data/processed", banks: list = None):
    """
    Computes required aggregate sentiment scores by bank and by star rating.
    Uses robust workspace matching to remain compatible with script and notebook runners.
    """
    if banks is None:
        banks = ["CBE", "Abyssinia", "Dashen"]
        
    print("\n" + "="*60)
    print(" OMEGA FINTECH ANALYTICS: AGGREGATED SENTIMENT REPORTS")
    print("="*60)
    

    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    marker = "fintech-review-analytics"
    
    if marker in current_file_dir:
        base_part = current_file_dir.split(marker)[0]
        project_root = os.path.join(base_part, marker)
    else:
        project_root = os.path.abspath(os.path.join(current_file_dir, "../.."))
    
    raw_source_path = os.path.join(project_root, "data/raw/raw_reviews.csv")
    
    
    if not os.path.isabs(target_dir):
        clean_target = target_dir.lstrip("./").replace("data/processed", "")
        target_dir = os.path.abspath(os.path.join(project_root, "data/processed", clean_target))
    
    for bank in banks:
        safe_name = bank.lower().replace(" ", "_")
        file_path = os.path.join(target_dir, f"{safe_name}_thematic_reviews.csv")
        
        if not os.path.exists(file_path):
            print(f" Warning: Staging file missing for processing: {file_path}")
            continue
            
        if not os.path.exists(raw_source_path):
            print(f" Error: Master landing file missing at coordinate: {raw_source_path}")
            return
            
        processed_df = pd.read_csv(file_path)
        raw_df = pd.read_csv(raw_source_path)
        
        merged_df = pd.merge(
            processed_df, 
            raw_df[['review', 'rating']], 
            left_on='review_text', 
            right_on='review', 
            how='inner'
        )
        
        if merged_df.empty:
            continue
        
        agg_summary = merged_df.groupby('rating')['sentiment_score'].mean().reset_index()
        agg_summary.columns = ['Star Rating', 'Mean Sentiment Confidence']
        
        print(f"\nBank: {bank}")
        print("-" * 35)
        print(agg_summary.to_string(index=False))
        print(f"📌 Distinct Business Themes Tracked: {processed_df['identified_theme'].nunique()}")
    print("="*60 + "\n")