import pandas as pd
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the reviews data"""
    if df.empty:
        return df
    
    initial = len(df)
    df = df.drop_duplicates(subset=['review', 'date', 'bank']).copy()
    df = df.dropna(subset=['review', 'rating']).copy()
    df['rating'] = df['rating'].astype(int)
    
    logger.info(f"Preprocessing: {initial:,} → {len(df):,} reviews "
                f"({len(df)/initial*100:.1f}%) kept")
    
    return df