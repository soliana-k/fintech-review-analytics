import pandas as pd
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_insights(df: pd.DataFrame):
    
    """Generate basic insights"""
    if df.empty:
        return
    
    logger.info("=== BUSINESS INSIGHTS ===")
    

    total = len(df)
    avg_rating = df['rating'].mean()
    pos = (df['sentiment_label'] == 'positive').sum()
    neg = (df['sentiment_label'] == 'negative').sum()
    
    logger.info(f"Total Reviews     : {total}")
    logger.info(f"Average Rating    : {avg_rating:.2f}/5")
    logger.info(f"Positive Sentiment: {pos/total*100:.1f}%")
    logger.info(f"Negative Sentiment: {neg/total*100:.1f}%")
    

    logger.info("\nPer Bank Summary:")
    summary = df.groupby('bank').agg(
        reviews=('review', 'count'),
        avg_rating=('rating', 'mean'),
        positive_pct=('sentiment_label', lambda x: (x == 'positive').mean() * 100)
    ).round(2)
    
    logger.info("\n" + str(summary))
    
    
    logger.info("\n Pipeline ready for deeper analysis!")