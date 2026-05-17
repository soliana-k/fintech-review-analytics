import os
import pandas as pd

def generate_analytics_report(target_dir: str = "data/processed", banks: list = None):
    """
    Computes required aggregate sentiment scores by bank and by star rating,
    fulfilling the final analytical requirements of Task 2.
    """
    if banks is None:
        banks = ["CBE", "Abyssinia", "Dashen"]
        
    print("\n" + "="*60)
    print(" OMEGA FINTECH ANALYTICS: AGGREGATED SENTIMENT REPORTS")
    print("="*60)
    
    for bank in banks:
        safe_name = bank.lower().replace(" ", "_")
        file_path = os.path.join(target_dir, f"{safe_name}_thematic_reviews.csv")
        raw_source_path = "data/raw/raw_reviews.csv"
        
        if not os.path.exists(file_path):
            continue
            
        
        processed_df = pd.read_csv(file_path)
        raw_df = pd.read_csv(raw_source_path)
        
       
        merged_df = pd.merge(
            processed_df, 
            raw_df[['review', 'rating']], 
            left_on='review_text', 
            right_on='review', 
            how='inner'
        )
        

        agg_summary = merged_df.groupby('rating')['sentiment_score'].mean().reset_index()
        agg_summary.columns = ['Star Rating', 'Mean Sentiment Confidence']
        
        print(f"\nBank: {bank}")
        print("-" * 35)
        print(agg_summary.to_string(index=False))
        print(f" Distinct Business Themes Tracked: {processed_df['identified_theme'].nunique()}")
    print("="*60 + "\n")