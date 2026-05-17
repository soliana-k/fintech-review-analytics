import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from transform.sentiment_pipeline import SentimentThematicTransformer

@pytest.fixture(scope="module")
def engine():
    return SentimentThematicTransformer()

def test_sentiment_outputs(engine):
    """Verifies compliance rules for generating correct labels and scores."""
    lbl, score = engine._extract_sentiment("This app is amazing and very fast!", 5)
    assert lbl in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

def test_tfidf_keyword_extraction(engine):
    """Verifies that explicit TF-IDF term arrays compile successfully."""
    corpus = ["login error system failure", "slow connection login delay timeout error"]
    keywords = engine.extract_top_tfidf_terms(corpus, top_n=2)
    assert len(keywords) <= 2
    assert "login" in keywords or "error" in keywords