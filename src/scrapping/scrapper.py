import pandas as pd
from google_play_scraper import Sort, reviews
import os
import time

APPS = {
    "CBE": "com.combanketh.mobilebanking",      
    "Abyssinia": "com.boa.boaMobileBanking",     
    "Dashen": "com.dashen.dashensuperapp",       

    
}

def scrape_data():
    all_data = []
    
    for bank_name, app_id in APPS.items():
        print(f"Scraping {bank_name}...")
        
        try:
            result, _ = reviews(
                app_id,
                lang='en', 
                country='et', 
                sort=Sort.NEWEST, 
                count=420 
            )
            
            if not result:
                print(f"No reviews found for {bank_name}. Retrying with local country code...")
                result, _ = reviews(app_id, lang='en', country='et', count=450)

            if result:
                df = pd.DataFrame(result)
                df = df[['content', 'score', 'at']].copy()
                df.columns = ['review', 'rating', 'date']
                
                df['bank'] = bank_name
                df['source'] = 'Google Play'
                
                all_data.append(df)
                print(f"Collected {len(df)} reviews for {bank_name}.")
            else:
                print(f"Failed to retrieve data for {bank_name}.")

        except Exception as e:
            print(f"Error scraping {bank_name}: {e}")
            
        time.sleep(2)

    if not all_data:
        print("No data collected at all. Check internet connection and App IDs.")
        return

    final_df = pd.concat(all_data, ignore_index=True)
    final_df = final_df.drop_duplicates(subset=['review', 'date', 'bank'])
    final_df['date'] = pd.to_datetime(final_df['date']).dt.strftime('%Y-%m-%d')
    final_df = final_df.dropna(subset=['review', 'rating'])
    os.makedirs('data/raw', exist_ok=True)
    final_df.to_csv('./data/raw/raw_reviews.csv', index=False)
    
    print("-" * 30)
    print(f"SAVED: data/raw/raw_reviews.csv")
    print(f"TOTAL: {len(final_df)} reviews collected.")

if __name__ == "__main__":
    scrape_data()