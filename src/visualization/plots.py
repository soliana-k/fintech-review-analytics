import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_visualizations(df: pd.DataFrame):
    """Create basic visualizations"""
    output_dir = Path("data/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 8))


    plt.subplot(2, 2, 1)
    sns.boxplot(data=df, x='bank', y='rating')
    plt.title('Rating Distribution by Bank')
    plt.xticks(rotation=45)

   
    plt.subplot(2, 2, 2)
    sentiment_counts = df['sentiment_label'].value_counts()
    sentiment_counts.plot(kind='bar')
    plt.title('Overall Sentiment Distribution')
    plt.xticks(rotation=0)

    
    plt.subplot(2, 2, 3)
    avg_ratings = df.groupby('bank')['rating'].mean()
    avg_ratings.plot(kind='bar')
    plt.title('Average Rating by Bank')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)


    plt.subplot(2, 2, 4)
    sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'], normalize='index') * 100
    sentiment_by_bank.plot(kind='bar', stacked=True)
    plt.title('Sentiment Distribution by Bank')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig(output_dir / "review_analysis.png", dpi=300, bbox_inches='tight')
    logger.info(f" Visualizations saved to {output_dir}/review_analysis.png")
    plt.close()