from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .base import SentimentStrategy

class VaderStrategy(SentimentStrategy):
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze(self, text: str):
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
            
        return {"label": label, "score": compound}