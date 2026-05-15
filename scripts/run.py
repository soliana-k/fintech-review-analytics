import pandas as pd
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config
from src.preprocessing.pipeline import clean_data
from src.nlp.sentiment.vader import VaderStrategy
from src.nlp.themes.extractor import extract_themes
from src.analytics.insights import generate_insights
from src.visualization.plots import create_visualizations
from src.scrapping.scrapper import scrape_data   

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Starting Fintech Review Analytics Pipeline")

    logger.info("Step 1: Running Scraper...")
    scrape_data()   # This will create data/raw/raw_reviews.csv

    raw_path = './data/raw/raw_reviews.csv'
    
    if not os.path.exists(raw_path):
        logger.error(f"Raw file not found at {raw_path}. Scraper failed.")
        return

    df = pd.read_csv(raw_path)
    logger.info(f"Loaded {len(df)} raw reviews from CSV")

    logger.info("Step 2: Preprocessing data...")
    df = clean_data(df)

    logger.info("Step 3: Performing Sentiment Analysis...")
    sentiment_strategy = VaderStrategy()
    
    sentiments = df['review'].apply(sentiment_strategy.analyze)
    df['sentiment_label'] = sentiments.apply(lambda x: x['label'])
    df['sentiment_score'] = sentiments.apply(lambda x: x['score'])

    logger.info(f"Sentiment analysis completed. Positive: {(df['sentiment_label'] == 'positive').sum()} | "
                   f"Negative: {(df['sentiment_label'] == 'negative').sum()}")

    logger.info("Step 4: Extracting Themes...")
    top_keywords, themes = extract_themes(df)


    config.CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    clean_path = config.CLEAN_DIR / "cleaned_reviews.csv"
    df.to_csv(clean_path, index=False)
    logger.info(f"Cleaned data saved to {clean_path}")

  
    logger.info("Step 5: Generating Insights and Plots...")
    generate_insights(df)
    create_visualizations(df)

    logger.info("🎉 Pipeline Completed Successfully!")
    logger.info(f"Total processed reviews: {len(df)}")


if __name__ == "__main__":
    main()