# AI Movie Recommendation Platform

An end-to-end AI-powered movie recommendation platform built with modern
Data Engineering, Machine Learning, semantic search, and local LLM technologies.

The platform processes MovieLens data through a Bronze/Silver/Gold data pipeline
and provides multiple recommendation strategies through an interactive Streamlit
dashboard.

---

## Project Status

**Status: Completed and tested**

- 27 automated tests passing
- Ruff static analysis passing
- End-to-end Streamlit dashboard verified
- Local Ollama integration verified

---

## Key Features

### Data Engineering

- MovieLens dataset ingestion
- CSV structural validation
- Centralized logging and path management
- Bronze/Silver/Gold data architecture
- PySpark ETL processing
- Explicit schema enforcement
- Data quality validation
- Parquet-based storage
- Gold-layer analytics and recommendation features

### Recommendation Engine

The platform combines multiple recommendation approaches:

- Popularity-based recommendation
- Content-based recommendation using TF-IDF
- Collaborative filtering
- Semantic recommendation using Sentence Transformers
- FAISS vector similarity search
- Hybrid recommendation ranking
- Score normalization and weighted ranking
- Configurable recommendation settings

### AI / LLM

- Natural-language movie search
- Query intent extraction
- Local Ollama LLM integration
- AI-generated recommendation explanations
- Prompt-based recommendation reasoning

### Dashboard

Built with Streamlit:

- Home page
- Movie title recommendation
- Fuzzy movie-title search and suggestions
- Natural-language AI search
- Recommendation movie cards
- Detailed recommendation table
- Genre analytics
- Movie rating analytics
- User preference analytics

---

## Architecture

```text
                    MovieLens Dataset
                           |
                           v
                  +------------------+
                  |    Ingestion     |
                  | Validation / DQ  |
                  +--------+---------+
                           |
                           v
                    Bronze Layer
                     Parquet
                           |
                           v
                  +------------------+
                  |    PySpark ETL   |
                  | Schema + Quality |
                  +--------+---------+
                           |
                           v
                    Silver Layer
                     Parquet
                           |
                           v
                  +------------------+
                  |   Gold Layer     |
                  | Analytics +      |
                  | Recommendation   |
                  | Features         |
                  +--------+---------+
                           |
              +------------+-------------+
              |            |             |
              v            v             v
        Content-based  Collaborative  Popularity
              |            |             |
              +------------+-------------+
                           |
                           v
                    Hybrid Ranking
                           |
              +------------+-------------+
              |                          |
              v                          v
       Movie Title Search        Semantic Search
                                  |
                           Sentence Transformer
                                  |
                                 FAISS
                                  |
                                  v
                         Recommendation Results
                                  |
                                  v
                           Ollama Explanation
                                  |
                                  v
                         Streamlit Dashboard
```

## Recommendation Flow
### Movie Title Recommendation
```text
User enters movie title
        |
        v
Movie Search / Title Resolution
        |
        v
Content + Collaborative + Popularity
        |
        v
Score Normalization
        |
        v
Weighted Hybrid Ranking
        |
        v
Top-N Recommendations
```

### Natural-Language Recommendation
```text
User query
    |
    v
Semantic Search
    |
    v
Sentence Transformer Embeddings
    |
    v
FAISS Similarity Search
    |
    v
Recommendation Ranking
    |
    v
Ollama
    |
    v
AI Explanation + Recommendations
```

## Data Architecture

The project follows a Medallion-style architecture.

```text
data/
├── raw/
│   ├── movies.csv
│   ├── ratings.csv
│   ├── tags.csv
│   └── links.csv
│
├── bronze/
│
├── silver/
│
└── gold/
```

### Bronze

Raw datasets are validated and converted into Parquet format.

### Silver

PySpark transformations perform:

- Schema enforcement
- Type standardization
- Timestamp conversion
- Text normalization
- Data quality validation

### Gold

Business-ready datasets contain:

- Movie metrics
- Genre metrics
- User preference profiles
- Recommendation features

## Technology Stack

| Category         | Technology |
|------------------| --- |
| Programming      | Python |
| Data Processing  | PySpark |
| Data Analysis    | Pandas, NumPy |
| Storage          | Parquet |
| Machine Learning | Scikit-learn |
| Embeddings       | Sentence Transformers |
| Vector Search    | FAISS |
| LLM              | Ollama |
| Dashboard        | Streamlit |
| Testing          | Pytest |
| Code Quality     | Ruff |
| Version Control  | Git |

## Project Structure
```text
ai-movie-recommendation-platform/
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── models/
│   └── faiss/
│
├── notebooks/
│
├── src/
│   ├── config/
│   ├── dashboard/
│   ├── embeddings/
│   ├── gold/
│   ├── ingestion/
│   ├── llm/
│   ├── recommendation/
│   ├── spark_jobs/
│   ├── utils/
│   └── vector_store/
│
├── tests/
│
├── docs/
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Setup
### 1. Clone the repository
```text
</> PowerShell
git clone <repository-url>
cd ai-movie-recommendation-platform
```
### 2. Create a virtual environment

Windows:
```text
</> PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
### 3. Install dependencies
```text
</> PowerShell
pip install -r requirements.txt
```
### 4. Prepare the MovieLens dataset

Place the MovieLens CSV files in:
```text
data/raw/
```
Required files:
```text
movies.csv
ratings.csv
tags.csv
links.csv
```

## Running the Data Pipeline
### Ingestion
```text
</> PowerShell
python -m src.ingestion.run_ingestion
```
### Silver ETL
```text
</> PowerShell
python -m src.spark_jobs.run_silver_etl
```
### Gold pipeline
```text
</> PowerShell
python -m src.gold.run_gold
```
### Build embeddings
```text
</> PowerShell
python -m src.embeddings.run_embeddings
```
## Running the Dashboard

Make sure Ollama is running locally when using AI Search.

Start Streamlit:
```text
</> PowerShell
python -m streamlit run src/dashboard/app.py
```
The dashboard provides:

- Movie title recommendations
- AI natural-language recommendations
- Recommendation details
- Analytics
## Testing

Run the complete test suite:
```text
</> PowerShell
python -m pytest -v
```
Current result:
```text
27 passed
```
Run Ruff:
```text
</> PowerShell
ruff check .
```
Current result:
```text
All checks passed!
```
## Recommendation Architecture

The hybrid recommendation engine combines:
```text
Content-Based
      +
Collaborative Filtering
      +
Popularity
      |
      v
Score Normalization
      |
      v
Weighted Hybrid Ranking
```
For natural-language queries:
```text
Natural Language Query
        |
        v
Semantic Search
        |
        v
FAISS
        |
        v
Recommendation Ranking
        |
        v
Ollama Explanation
```
## Data Quality

The pipeline includes validation for:

- Required columns
- Null values
- Duplicate keys
- Numeric ranges
- Empty strings
- Schema mismatches

Automated tests cover these validation rules.
## License

This project is intended as a portfolio and learning project.
