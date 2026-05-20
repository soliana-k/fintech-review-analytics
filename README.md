# Fintech Review Analytics

## Customer Review Analytics for Ethiopian Banking Apps

A Python-based ETL and NLP pipeline that collects, analyzes, and visualizes Google Play Store reviews for major Ethiopian banking apps:

* Commercial Bank of Ethiopia (CBE)
* Dashen Bank
* Bank of Abyssinia

The project transforms raw customer feedback into structured sentiment and thematic insights that help identify usability issues, app stability problems, and customer pain points.

---

# Project Objective

The goal of this project is to analyze customer experience trends across Ethiopian fintech applications using real-world review data.

The pipeline:

* Scrapes live Google Play reviews
* Cleans and preprocesses raw text
* Performs sentiment analysis
* Detects recurring complaint themes
* Stores processed data in PostgreSQL
* Generates analytical visualizations

---

# Tech Stack

## Core Technologies

* Python 3.10+
* PostgreSQL
* SQLAlchemy

## Data Collection

* google-play-scraper

## Data Processing

* pandas
* NumPy

## NLP & Machine Learning

* DistilBERT
* VADER Sentiment
* spaCy
* TF-IDF

## Visualization

* Matplotlib
* Seaborn

---

# Project Structure

```text
fintech-review-analytics/
│
├── scripts/
│   └── run.py
│
├── notebooks/
│   └── main.ipynb
│
├── database/
│   └── schema.sql
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── plots/
│
├── src/
│   ├── scraping/
│   │   ├── __init__.py
│   │   └── scraper.py
│   │
│   ├── transformers/
│   │   └── sentiment_transformer.py
│   │
│   ├── storage/
│   │   └── db_loader.py
│   │
│   └── pipelines/
│       ├── etl_bank_pipeline.py
│       ├── aggregation_reporter.py
│       └── dashboard_plots.py
│
├── requirements.txt
├── main.py
└── README.md
```

---

# ETL Pipeline Overview

## 1. Extract

Reviews are scraped directly from the Google Play Store using `google-play-scraper`.

### The extraction layer:

* Pulls review text, ratings, and metadata
* Filters non-English reviews
* Saves raw data locally

---

## 2. Transform

### Sentiment Analysis

The project uses:

* DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`)
* VADER sentiment scoring

Since DistilBERT is a binary classifier (`POSITIVE` / `NEGATIVE`), a hybrid rule-based approach was added to support a third `NEUTRAL` class.

Neutral sentiment is assigned when:

* The review has a 3-star rating
* OR the VADER compound score falls within a neutral threshold

This improves handling of mixed or ambiguous feedback.

---

### Text Preprocessing

Text preprocessing is performed using spaCy:

* Lowercasing
* Tokenization
* Stop-word removal
* Lemmatization

---

### Theme Classification

Reviews are grouped into operational themes using keyword-based matching.

Themes include:

* Account Access Issues
* Transaction Performance
* UI & Design
* Customer Support
* Feature Requests
* General Feedback

---

## 3. Load

Processed review data is stored in:

* CSV outputs
* PostgreSQL relational tables

The database schema includes:

* `banks`
* `reviews`

with foreign key relationships for normalization and integrity.

---

# Database Integration

## Database System

* PostgreSQL
* SQLAlchemy ORM

## Integrity Checks

Post-ingestion validation included:

* Review count verification
* Average rating aggregation
* Null value checks

---

## Final Dataset Summary

| Bank      | Reviews | Average Rating |
| --------- | ------- | -------------- |
| Dashen    | 585     | 4.06           |
| CBE       | 494     | 3.76           |
| Abyssinia | 494     | 2.90           |

A total of 1,573 reviews were processed successfully.

---

# Visualizations

The project generates multiple analytical charts, including:

* Sentiment distribution per bank
* Rating distribution analysis
* Negative review pain-point analysis
* Theme frequency heatmaps

Generated plots are saved under:

```text
data/plots/
```

---

# Key Insights

## Dashen Bank

* Highest positive sentiment share
* Strong UI and usability feedback
* Some complaints related to transaction delays

## Commercial Bank of Ethiopia

* Stable overall sentiment
* Recurring complaints tied to login and update-related issues

## Bank of Abyssinia

* Highest negative sentiment share
* Frequent reports of crashes and stability issues

---

# Running the Project

## Clone the Repository

```bash
git clone <repo-url>
cd fintech-review-analytics
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Pipeline

```bash
python main.py
```

---

# Output Files

After execution, the pipeline generates:

```text
data/processed/
data/plots/
```

Including:

* Processed review datasets
* Sentiment analytics
* Visualization assets

---

# Future Improvements

Potential extensions include:

* Real-time dashboard deployment
* Topic modeling with BERTopic or LDA
* Multilingual sentiment support
* Automated scheduling with Airflow
* Cloud-based data storage and orchestration

---

# Author

**Kalkidan Kassahun**

Built as a practical NLP + Data Engineering project focused on customer experience analytics in Ethiopian fintech systems.
