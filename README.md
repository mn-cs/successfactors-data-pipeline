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

## 🔗 Quick Links

- [Included Dataset Snapshot (CSV)](data/interim/merged_dataset_2025-09-04.csv)
- [Exploratory Analysis Notebook](notebooks/0.01-mb-data-exploration.ipynb)
- [Data Cleaning Workflow](notebooks/1.01-mb-data-cleaning.ipynb)
- [Visualization Notebook](notebooks/2.01-mb-visualization.ipynb)
- [Education Split Notebook](notebooks/edu_split.ipynb)
- [Dataset Merge Notebook](notebooks/merge.ipynb)

## 🚀 Quick Start

### Prerequisites

- Python 3.12 recommended
- `uv`
- A valid `RAPIDAPI_KEY` in `.env`
- Docker/PostgreSQL only if you want the optional database workflow

### Installation

Install the project and development dependencies from `pyproject.toml` and `uv.lock`:

```bash
make install
```

This runs:

```bash
uv sync --frozen --extra dev
```

### Run The Pipeline

```bash
make run
```

This command:

- fetches the latest Forbes data
- reuses existing Wikipedia scrape files if they already exist
- otherwise scrapes missing Wikipedia birth-date and education data
- writes the merged output to `data/processed/merged_dataset_<YYYY-MM-DD>.csv`

### Use The Included Data

This repository already includes generated data files under `data/`, including:

- `data/external/api_fetched/`
- `data/external/web_scraped/`
- `data/interim/`
- `data/processed/`

If you only want to inspect the latest results, you can open the latest CSV in `data/processed/` without rerunning the pipeline.

### Scrape Limit

When the pipeline needs to generate fresh Wikipedia scrape files, it limits scraping to `10` people by default.

You can change that with `SCRAPE_LIMIT`:

```bash
SCRAPE_LIMIT=10 make run
SCRAPE_LIMIT=100 make run
SCRAPE_LIMIT=all make run
```

Notes:

- `SCRAPE_LIMIT=all` removes the limit and attempts to scrape every Forbes row.
- If scrape files already exist in `data/external/web_scraped/`, `make run` will reuse them.
- To force a new scrape with a different limit, delete or rename the existing `wiki_date_of_birth_*.csv` and `wiki_university_degree_*.csv` files first.
- The merged dataset still contains the full Forbes row set. The scrape limit only controls how many rows get newly scraped Wikipedia enrichment during regeneration.

### Scrape Only

If you want to refresh only the Wikipedia scrape inputs:

```bash
make scrape
```

### Optional Database Workflow

`make run` does not require PostgreSQL.

If you want the database container for SQL work, start it with:

```bash
docker compose up -d db
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

```text
├── data/
│   ├── external/
│   │   ├── api_fetched/
│   │   └── web_scraped/
│   ├── interim/
│   └── processed/
├── notebooks/
├── src/
│   ├── api_fetchers/
│   ├── data_transformers/
│   ├── modeling/
│   ├── scrapers/
│   ├── sql/
│   ├── config.py
│   ├── dataset.py
│   ├── features.py
│   └── plots.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── uv.lock
```

---

## 🔧 Development

### Code Quality

```bash
make lint      # Check code style
make format    # Format code
```

### Common Commands

```bash
make help      # List available commands
make install   # Install dependencies with uv
make scrape    # Refresh the Wikipedia scrape files
make run       # Run the full pipeline
```

### Database Operations

```bash
docker compose up -d db
```

### Jupyter Notebooks

```bash
uv run jupyter lab
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

---
