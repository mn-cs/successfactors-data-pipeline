# SuccessFactors Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)](https://www.postgresql.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **⚠️ Development Status**: This project is currently under active development and is not yet complete. Features and documentation may change as development progresses.

A comprehensive data science project that collects and analyzes profiles of successful individuals through APIs and web scraping to identify common traits, educational patterns, and career paths that contribute to extraordinary success.

## 🎯 Project Overview

This project combines data collection, transformation, and machine learning to:

- **Collect** billionaire profiles from Forbes API
- **Scrape** biographical data from Wikipedia
- **Analyze** educational backgrounds and career patterns
- **Model** success factors and predictive traits
- **Visualize** insights through interactive dashboards

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- PostgreSQL (via Docker)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/micben-cs/successfactors.git
cd successfactors
```

2. **Set up virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

5. **Start the database**

```bash
docker-compose up -d
```

6. **Run the project**

```bash
python -m successfactors
```

## 📊 Data Pipeline

The project follows a structured ETL pipeline:

1. **Extract**: Fetch data from Forbes API and scrape Wikipedia
2. **Transform**: Clean, normalize, and merge datasets
3. **Load**: Store in PostgreSQL with proper schema
4. **Analyze**: Generate insights and train ML models

### Data Sources

- **Forbes Billionaires API**: Financial and demographic data
- **Wikipedia**: Educational backgrounds and biographical details

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Data Processing**: pandas, numpy, scikit-learn
- **Web Scraping**: BeautifulSoup4, httpx, requests-cache
- **Database**: PostgreSQL, SQLAlchemy
- **Notebooks**: Jupyter Lab
- **Containerization**: Docker, Docker Compose
- **Code Quality**: Ruff (linting & formatting), pytest
- **Documentation**: MkDocs

## 📁 Project Structure

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
│   └── sql_connections  <- Database connection examples and methods in Jupyter Notebook
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
    ├── sql                     <- SQL scripts organized by purpose
    │   ├── analytics           <- Analytical queries and data exploration SQL
    │   ├── commands.md         <- SQL command documentation and examples
    │   ├── schema              <- Database schema definitions and table creation scripts
    │   └── staging             <- Data staging and ETL SQL scripts
    │
    └── web_scrapers            <- Scripts to scrape data from websites
```

---

## 🔧 Development

### Running Tests

```bash
make test
# or
pytest tests/
```

### Code Quality

```bash
make lint      # Check code style
make format    # Format code
```

### Database Operations

```bash
# Start PostgreSQL container
docker-compose up -d

# Run database migrations
make migrate

# Access database directly
docker exec -it success-db-y psql -U $POSTGRES_USER -d $POSTGRES_DB
```

### Jupyter Notebooks

```bash
jupyter lab
# Navigate to notebooks/ directory
```

## 📈 Key Features

- **🔍 Data Collection**: Automated API fetching and web scraping
- **🧹 Data Cleaning**: Robust ETL pipeline with data validation
- **🏗️ Database**: Structured PostgreSQL schema with indexes
- **📊 Analysis**: Statistical analysis and pattern recognition
- **🤖 ML Modeling**: Predictive models for success factors
- **📝 Documentation**: Comprehensive docs with MkDocs
- **🐳 Containerized**: Full Docker support for reproducibility

## 🗂️ Data Schema

### Main Tables

- **billionaires**: Core demographic and financial data
- **education**: University degrees and academic backgrounds
- **careers**: Professional history and industry patterns

### Key Metrics

- Net worth trends and distributions
- Educational institution rankings
- Industry success patterns
- Geographic concentration analysis

## 📚 Documentation

Full documentation is available in the `docs/` directory:

- [Getting Started Guide](docs/docs/getting-started.md)
- [Data Codebook](docs/docs/codebook.md)
- [API Documentation](docs/)

Build docs locally:

```bash
cd docs
mkdocs serve
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines (enforced by Ruff)
- Write tests for new features
- Update documentation as needed
- Use conventional commit messages

## 📋 Roadmap

- [ ] **Phase 1**: Data collection and cleaning ✅
- [ ] **Phase 2**: Database schema and ETL pipeline ✅
- [ ] **Phase 3**: Exploratory data analysis (In Progress)
- [ ] **Phase 4**: Machine learning models
- [ ] **Phase 5**: Web dashboard and visualization
- [ ] **Phase 6**: API for external access

## ⚠️ Limitations

- Data limited to publicly available information
- Forbes API rate limiting may affect data collection speed
- Wikipedia scraping subject to website changes
- Educational data may be incomplete for some individuals

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Forbes for providing billionaire data through their API
- Wikipedia for biographical information
- Open source community for the amazing tools and libraries

## 📞 Contact

**Michael** - [@micben-cs](https://github.com/micben-cs)

Project Link: [https://github.com/micben-cs/successfactors](https://github.com/micben-cs/successfactors)

---

_Built with ❤️ for data science and success analysis_
