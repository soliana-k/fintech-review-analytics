from transformers import pipeline
from .base import SentimentStrategy

class BertStrategy(SentimentStrategy):
    def __init__(self):
        self.classifier = pipeline("sentiment-analysis", 
                                 model="distilbert-base-uncased-finetuned-sst-2-english")
    
    def analyze(self, text: str):
        if not text or len(text.strip()) < 5:
            return {"label": "neutral", "score": 0.0}
        
        result = self.classifier(text[:512])[0] 
        label = result['label'].lower()
        score = result['score'] if label == 'positive' else -result['score']
        return {"label": label, "score": score}