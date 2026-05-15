import pandas as pd
import re
from collections import Counter
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_themes(df: pd.DataFrame, top_n: int = 10):
    """Extract common themes and keywords"""
    if df.empty:
        return [], {}
    
    text = " ".join(df['review'].astype(str)).lower()
   
    words = re.findall(r'\b\w+\b', text)
    stop_words = {"the", "and", "is", "in", "to", "of", "for", "on", "app", "this", "that", "with"}
    words = [w for w in words if w not in stop_words and len(w) > 3]
    
    top_keywords = Counter(words).most_common(top_n)
    
    themes = {
        "Login & Access": ["login", "password", "access", "sign", "account"],
        "Transaction Issues": ["transfer", "send", "money", "failed", "slow", "transaction"],
        "App Performance": ["slow", "crash", "loading", "freeze", "update"],
        "UI/Experience": ["ui", "design", "easy", "good", "great", "bad"],
        "Customer Support": ["support", "customer", "help", "call", "service"]
    }
    
    logger.info(f"Top {top_n} Keywords: {top_keywords}")
    return top_keywords, themes