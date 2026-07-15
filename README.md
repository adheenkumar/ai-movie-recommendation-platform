# AI Movie Recommendation Platform

An end-to-end AI-powered movie recommendation system built with:

- PySpark
- Streamlit
- Ollama
- FAISS
- Sentence Transformers
- SQLite/PostgreSQL

## Project Status

### Sprint 1 - Project Setup

- [x] Repository initialization
- [x] Project structure
- [x] Python package structure
- [x] Virtual environment setup

### Sprint 2 - Data Ingestion and Bronze Layer

- [x] MovieLens raw dataset integration
- [x] Centralized logging
- [x] Centralized path management
- [x] CSV structural validation
- [x] Reusable dataset ingestion engine
- [x] Multi-dataset ingestion orchestration
- [x] Bronze Parquet layer
- [x] Automated data quality profiling
- [x] Pytest quality report validation

### Sprint 3 - PySpark Silver ETL

- [x] Centralized Spark session configuration
- [x] Bronze schema inspection
- [x] Explicit Silver schema contracts
- [x] Bronze-to-Silver PySpark transformations
- [x] Unix timestamp conversion
- [x] Text normalization
- [x] Identifier type standardization
- [x] Schema contract validation
- [x] Required-column validation
- [x] Unique-key validation
- [x] Numeric-range validation
- [x] Non-empty string validation
- [x] Silver Parquet output
- [x] Automated PySpark regression tests

### Sprint 4 - Gold Analytics and Recommendation Features

- [ ] Movie rating aggregates
- [ ] Popularity metrics
- [ ] Bayesian weighted rating score
- [ ] Genre-level analytics
- [ ] User preference profiles
- [ ] Recommendation feature dataset
- [ ] Gold schema validation
- [ ] Gold Parquet output