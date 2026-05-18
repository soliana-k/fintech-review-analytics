import pandas as pd
from google_play_scraper import Sort, reviews
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

APPS = {
    "CBE": "com.combanketh.mobilebanking",      
    "Abyssinia": "com.boa.boaMobileBanking",     
    "Dashen": "com.dashen.dashensuperapp",       
}

def scrape_data():
    all_data = []
    
    for bank_name, app_id in APPS.items():
        logger.info(f"Scraping {bank_name}...")
        
        try:
            result, _ = reviews(
                app_id,
                lang='en', 
                country='us', 
                sort=Sort.NEWEST, 
                count=800 
            )
            
            if not result:
                logger.warning(f"No reviews found for {bank_name}. Retrying...")
                result, _ = reviews(app_id, lang='en', country='us', count=800)

            if result:
                df = pd.DataFrame(result)
                df = df[['content', 'score', 'at']].copy()
                df.columns = ['review', 'rating', 'date']
                
                df['bank'] = bank_name
                df['source'] = 'Google Play'
                
                all_data.append(df)
                logger.info(f"Collected {len(df)} reviews for {bank_name}.")
            else:
                logger.warning(f"No data returned for {bank_name}")

        except Exception as e:
            logger.error(f"Error scraping {bank_name}: {e}")
            
        time.sleep(2)

    if not all_data:
        logger.error("No data collected at all.")
        return

    final_df = pd.concat(all_data, ignore_index=True)
    final_df = final_df.drop_duplicates(subset=['review', 'date', 'bank'])
    final_df['date'] = pd.to_datetime(final_df['date']).dt.strftime('%Y-%m-%d')
    final_df = final_df.dropna(subset=['review', 'rating'])

    os.makedirs('data/raw', exist_ok=True)
    final_df.to_csv('./data/raw/raw_reviews.csv', index=False)
    
    logger.info(f"SAVED: data/raw/raw_reviews.csv | TOTAL: {len(final_df)} reviews")


if __name__ == "__main__":
    scrape_data()