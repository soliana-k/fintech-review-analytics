import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class FintechVisualizer:
    def __init__(self):
        user, pw = os.getenv("DB_USER"), os.getenv("DB_PASSWORD")
        host, port = os.getenv("DB_HOST"), os.getenv("DB_PORT")
        db = os.getenv("DB_NAME")
        self.engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.output_dir = os.path.join(base_dir, "data", "plots")
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_data(self):
        query = """
        SELECT r.sentiment_label, r.identified_theme, r.rating, r.review_date, b.bank_name 
        FROM reviews r
        JOIN banks b ON r.bank_id = b.bank_id
        """
        df = pd.read_sql(query, self.engine)
        df['review_date'] = pd.to_datetime(df['review_date'])
        return df

    def generate_plots(self):
        df = self.fetch_data()
        sns.set_theme(style="whitegrid", palette="muted")
        
        # VISUAL 1: Sentiment Distribution Breakdown
        plt.figure(figsize=(10, 6))
        sentiment_pct = df.groupby('bank_name')['sentiment_label'].value_counts(normalize=True).unstack() * 100
        sentiment_pct = sentiment_pct[['NEGATIVE', 'NEUTRAL', 'POSITIVE']]
        
        ax = sentiment_pct.plot(kind='bar', stacked=True, color=['#e74c3c', '#f1c40f', '#2ecc71'], ax=plt.gca(), width=0.45)
        for container in ax.containers:
            labels = [f'{v.get_height():.1f}%' if v.get_height() > 2 else '' for v in container]
            ax.bar_label(container, labels=labels, label_type='center', fontweight='bold', color='black', fontsize=10)

        plt.title('Market Sentiment Share: Who is Winning User Trust?', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Bank Name', fontweight='bold', fontsize=11)
        plt.ylabel('Percentage of Total Reviews (%)', fontweight='bold', fontsize=11)
        plt.xticks(rotation=0)
        plt.ylim(0, 110) 
        plt.legend(title='User Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'sentiment_distribution.png'), dpi=300)
        plt.close()

        # VISUAL 2: Rating Spread & Dispersion
        plt.figure(figsize=(10, 5))
        sns.boxplot(data=df, x='bank_name', y='rating', palette='Set2', width=0.4)
        plt.title('User Rating Spread & Dispersion per Competitor', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Bank Name', fontweight='bold', fontsize=11)
        plt.ylabel('Rating Score (1-5 Stars)', fontweight='bold', fontsize=11)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'rating_distribution.png'), dpi=300)
        plt.close()

        # VISUAL 3: Critical Pain Points (Negative Reviews Only)
        plt.figure(figsize=(11, 5))
        negative_df = df[df['sentiment_label'] == 'NEGATIVE']
        top_neg_themes = negative_df['identified_theme'].value_counts().nlargest(5).index
        filtered_neg = negative_df[negative_df['identified_theme'].isin(top_neg_themes)]
        
        sns.countplot(data=filtered_neg, y='identified_theme', hue='bank_name', palette='Reds_r')
        plt.title('Top 5 System Pain Points (Negative Reviews Only)', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Complaint Volume Count', fontweight='bold', fontsize=11)
        plt.ylabel('Identified Issue / Theme', fontweight='bold', fontsize=11)
        plt.legend(title='Bank Name')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'sentiment_trend.png'), dpi=300)
        plt.close()

       
        # VISUAL 4: Cross-Tabulation Density Heatmap
        plt.figure(figsize=(9, 5))
        heatmap_data = pd.crosstab(df['identified_theme'], df['bank_name'])
        sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", cbar=True)
        plt.title('Cross-Tabulation Density Heatmap: Themes vs. Banks', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Bank Name', fontweight='bold', fontsize=11)
        plt.ylabel('Identified System Theme', fontweight='bold', fontsize=11)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'theme_intensity_heatmap.png'), dpi=300)
        plt.close()

        print(f" Success! 4 synchronized analytical plots saved to: {self.output_dir}")

if __name__ == "__main__":
    visualizer = FintechVisualizer()
    visualizer.generate_plots()