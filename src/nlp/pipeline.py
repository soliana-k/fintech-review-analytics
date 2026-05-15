import pandas as pd
from .sentiment.base import SentimentStrategy

class NLPPipeline:
    def __init__(self, sentiment_strategy: SentimentStrategy):
        self.sentiment_strategy = sentiment_strategy
    
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        results = []
        for _, row in df.iterrows():
            sentiment = self.sentiment_strategy.analyze(row['review'])
            results.append({
                'sentiment_label': sentiment['label'],
                'sentiment_score': sentiment['score']
            })
        
        df = pd.concat([df.reset_index(drop=True), 
                       pd.DataFrame(results)], axis=1)
        return df