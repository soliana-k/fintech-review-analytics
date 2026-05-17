import pandas as pd
import torch
import spacy
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentThematicTransformer:
    """
    Stateless Compute Engine responsible strictly for data transformations (T).
    Handles NLP inference and keyword text engineering.
    """
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
            
        device = 0 if torch.cuda.is_available() else -1
        self.classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=device
        )
        
        self.vader = SentimentIntensityAnalyzer()
        
        self.theme_rules = {
            "Account Access Issues": ["login", "password", "sign", "error", "unable", "lock", "block", "deny"],
            "Transaction Performance": ["slow", "loading", "delay", "timeout", "network", "pending", "transfer", "fail", "stuck"],
            "UI & Design": ["interface", "design", "beautiful", "clean", "confusing", "look", "layout", "color", "screen"],
            "Customer Support": ["help", "support", "call", "agent", "branch", "service", "respond", "complain"],
            "Feature Requests": ["fingerprint", "biometric", "otp", "code", "update", "notification", "alert", "budgeting"]
        }

    def _preprocess_text(self, text: str) -> str:
        """Pipeline Transform: Handles tokenization, stop-word removal, and lemmatization."""
        if not isinstance(text, str) or text.strip() == "":
            return ""
        doc = self.nlp(text.lower())
        return " ".join([t.lemma_ for t in doc if not t.is_stop and not t.is_punct])

    def _extract_sentiment(self, text: str, rating: int) -> tuple[str, float]:
        """Pipeline Transform: Runs hybrid NLP scoring to resolve the 3-Class target space."""
        if not isinstance(text, str) or text.strip() == "":
            return "NEUTRAL", 0.0
            
        truncated_text = text[:512] 
        try:
            bert_res = self.classifier(truncated_text)[0]
            label = bert_res['label']
            score = bert_res['score']
            
            
            vader_compound = self.vader.polarity_scores(truncated_text)['compound']
            
            if abs(vader_compound) < 0.15 or rating == 3:
                return "NEUTRAL", float(1.0 - abs(vader_compound))
                
            normalized_label = "POSITIVE" if label == "POSITIVE" else "NEGATIVE"
            return normalized_label, float(score)
        except Exception:
            return "NEUTRAL", 0.0

    def _map_theme(self, cleaned_text: str) -> str:
        """Pipeline Transform: Maps preprocessed tokens into business-relevant themes."""
        if not cleaned_text:
            return "General Feedback"
        for theme, keywords in self.theme_rules.items():
            if any(word in cleaned_text for word in keywords):
                return theme
        return "General Feedback"

    def transform_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes Vector/Row Transformations on the loaded dataset chunk.
        """
        if df.empty:
            return df
            
       
        working_df = df.copy()
        
        
        working_df['cleaned_text'] = working_df['review'].apply(self._preprocess_text)
        
        
        sentiment_outputs = [
            self._extract_sentiment(row['review'], row['rating']) 
            for _, row in working_df.iterrows()
        ]
        working_df['sentiment_label'] = [res[0] for res in sentiment_outputs]
        working_df['sentiment_score'] = [res[1] for res in sentiment_outputs]
        
        
        working_df['identified_theme'] = working_df['cleaned_text'].apply(self._map_theme)
        
        #
        working_df.insert(0, 'review_id', range(1, len(working_df) + 1))
        
        final_df = working_df[['review_id', 'review', 'sentiment_label', 'sentiment_score', 'identified_theme']].copy()
        final_df.columns = ['review_id', 'review_text', 'sentiment_label', 'sentiment_score', 'identified_theme']
        
        return final_df