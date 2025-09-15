# SuccessFactors

> **⚠️ Development Status**: This project is currently under active development and is not yet complete. Features and documentation may change as development progresses.

A data science project that collects profiles of successful individuals through APIs to analyze common traits and career paths.

## Project Organization

```
├── .dockerignore        <- Docker ignore file for build optimization   ┐
├── .env                 <- Environment variables (API keys, secrets)   │ <- not in version control
├── .gitignore           <- Git ignore file specifying untracked files. │
├── .venv/               <- Virtual environment directory               ┘
├── docker-compose.yml   <- Docker Compose configuration for multi-container setup
├── Dockerfile           <- Docker container configuration
├── LICENSE              <- MIT License for open-source distribution
├── Makefile             <- Makefile with convenience commands like `make data` or `make train`
├── README.md            <- The top-level README for developers using this project.
├── data
│   ├── external         <- Data from third party sources.
│   │   ├── API_fetched  <- Raw JSON data retrieved from APIs (e.g., Forbes billionaires)
│   │   └── web_scraped  <- CSV data scraped from websites (e.g., Wikipedia biographical info)
│   ├── interim          <- Intermediate data that has been transformed.
│   ├── processed        <- The final, canonical data sets for modeling.
│   └── raw              <- The original, immutable data dump.
│
├── docs                 <- A default mkdocs project; see www.mkdocs.org for details
│
├── models               <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks            <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml       <- Project configuration file with package metadata for
│                         successfactors and configuration for tools like black
│
├── references           <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports              <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures          <- Generated graphics and figures to be used in reporting
│
├── requirements.txt     <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── requirements-dev.txt <- Development dependencies for testing and code quality
│
├── tests/               <- Unit tests and test fixtures
│
└── successfactors       <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes successfactors a Python module
    │
    ├── __main__.py             <- Entry point for running the package as a module
    │
    ├── api_fetchers            <- Scripts to fetch data from external APIs
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── data_transformers       <- Scripts to clean and transform raw data
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling
    │   ├── __init__.py
    │   ├── predict.py          <- Code to run model inference with trained models
    │   └── train.py            <- Code to train models
    │
    ├── plots.py                <- Code to create visualizations
    │
    ├── processors              <- Data processing utilities and pipelines
    │
    ├── sql                     <- SQL scripts for database operations and queries
    │
    └── web_scrapers            <- Scripts to scrape data from websites
```

---
