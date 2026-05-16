# Fintech Review Analytics

**Automated Sentiment & Thematic Analysis of Ethiopian Banking Apps**

A robust data pipeline that scrapes, cleans, analyzes, and visualizes customer reviews from Google Play Store for major Ethiopian banks — **CBE, Abyssinia, and Dashen**.

---

## 🎯 Project Objective

To collect, analyze, and derive actionable business insights from customer reviews of Ethiopian fintech/banking mobile applications. This project helps banks understand customer satisfaction, identify pain points, and make data-driven product improvements.

### Key Goals
- Scrape high-quality reviews from Google Play Store
- Perform sentiment and thematic analysis
- Generate business insights and visualizations
- Build a maintainable, modular, and extensible codebase

---

## 🏗️ Architecture & Design

This project follows **Layered Architecture** with strong **Separation of Concerns** and modern design patterns:

- **Strategy Pattern** – For flexible sentiment analysis (easily switch between VADER, BERT, etc.)
- **Pipeline Pattern** – For preprocessing steps
- **Modular Design** – Clear separation between Ingestion, Preprocessing, NLP, Analytics, and Visualization layers

### Tech Stack

- **Python 3.10+**
- **Scraping**: `google-play-scraper`
- **Data Processing**: pandas, NumPy
- **NLP / Sentiment**: VADER (primary), ready for DistilBERT
- **Visualization**: Matplotlib, Seaborn
- **Logging**: Logging
- **Configuration**: Custom Config class

---

## 📁 Project Structure

```bash
fintech-review-analytics/
├── src/
│   ├── config.py
│   ├── scrapping/
│   ├── preprocessing/
│   ├── nlp/
│   │   ├── sentiment/
│   │   └── themes/
│   ├── analytics/
│   └── visualization/
├── scripts/
│   └── run.py          # Main ETL pipeline
├── data/
│   ├── raw/
│   └── cleaned/
|   └── visualization/
├── sql/                         # (Future)
├── .github/workflows/           # CI/CD
├── requirements.txt
├── .gitignore
└── README.md
