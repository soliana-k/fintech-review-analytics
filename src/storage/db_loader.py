import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

class BankDBLoader:
    def __init__(self):
        user = os.getenv("DB_USER")
        pw = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        db = os.getenv("DB_NAME")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.schema_path = os.path.join(current_dir, "..", "..", "database", "schema.sql")
        self.engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")

    def initialize_database(self):
        """Reads the schema.sql file and executes it to set up tables."""
        if not os.path.exists(self.schema_path):
            print(f"Schema file not found at {self.schema_path}")
            return

        with open(self.schema_path, "r") as f:
            schema_sql = f.read()

        with self.engine.connect() as conn:
            conn.execute(text(schema_sql))
            conn.commit()
            print(" Database schema initialized successfully.")

    def migrate_csv_to_sql(self, processed_path, raw_path, bank_name):
        
        df_p = pd.read_csv(processed_path)
        df_r = pd.read_csv(raw_path)
        
        final_df = pd.merge(
            df_p, 
            df_r[['review', 'rating']], 
            left_on='review_text', 
            right_on='review', 
            how='inner'
        ).drop(columns=['review'])

        
        with self.engine.connect() as conn:
            query = text("SELECT bank_id FROM banks WHERE bank_name = :name")
            b_id = conn.execute(query, {"name": bank_name}).scalar()

        if b_id is None:
            print(f"Error: {bank_name} not found in 'banks' table.")
            return

        final_df['bank_id'] = b_id
        if 'review_id' in final_df.columns:
            final_df = final_df.drop(columns=['review_id'])

    
        final_df.to_sql('reviews', self.engine, if_exists='append', index=False)
        print(f"Successfully migrated {len(final_df)} records for {bank_name}.")

    def verify_integrity(self):
        """Runs SQL queries to verify data was loaded correctly."""
        print("\n--- 🔍 Data Integrity Report ---")
        
        with self.engine.connect() as conn:
            
            print("1. Reviews per Bank:")
            res_count = conn.execute(text("""
                SELECT b.bank_name, COUNT(r.review_id) 
                FROM reviews r 
                JOIN banks b ON r.bank_id = b.bank_id 
                GROUP BY b.bank_name;
            """))
            for row in res_count:
                print(f"   - {row[0]}: {row[1]} reviews")

            
            print("\n2. Average Rating per Bank:")
            res_avg = conn.execute(text("""
                SELECT b.bank_name, ROUND(AVG(r.rating), 2) 
                FROM reviews r 
                JOIN banks b ON r.bank_id = b.bank_id 
                GROUP BY b.bank_name;
            """))
            for row in res_avg:
                print(f"   - {row[0]}: {row[1]} stars")

           
            print("\n3. Null Check (Critical Columns):")
            res_nulls = conn.execute(text("""
                SELECT 
                    SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) as null_text,
                    SUM(CASE WHEN sentiment_label IS NULL THEN 1 ELSE 0 END) as null_sentiment,
                    SUM(CASE WHEN bank_id IS NULL THEN 1 ELSE 0 END) as null_bank
                FROM reviews;
            """)).fetchone()
            
            print(f"   - Null Reviews: {res_nulls[0]}")
            print(f"   - Null Sentiments: {res_nulls[1]}")
            print(f"   - Null Bank IDs: {res_nulls[2]}")
            
        print("-------------------------------\n")

