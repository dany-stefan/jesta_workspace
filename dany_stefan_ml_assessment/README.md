# Senior ML Engineer Technical Assessment
**Candidate:** Dany Stefan  
**Position:** Senior MLOps Engineer  
**Date:** February 2026

## Overview
This assessment demonstrates ML engineering capabilities for demand forecasting in retail/fashion, including strategic analysis, feature engineering, and production-ready code.

## Project Structure
```
dany_stefan_ml_assessment/
├── README.md                    # This file
├── strategy_analysis.md         # Part 1: Strategic analysis (Tasks 1-3)
├── tmp_answers.md              # Working notes and answers
├── tmp_answers_part2.ipynb     # Part 2: Experimental work (Polars + Pandas comparison)
├── engineering.ipynb            # Part 2: ML engineering work (Tasks 4-5)
├── production_code.py           # Part 2: Production-ready code (Task 6)
├── requirements.txt             # Python dependencies
├── presentation.html            # Technical presentation (10-12 slides)
└── data/
    └── fashion_sample.csv       # Sample data (100 days, 1 product, 1 store)
```

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip

### Installation
```bash
# Navigate to project directory
cd dany_stefan_ml_assessment

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import polars as pl; print(f'Polars {pl.__version__} installed successfully')"
```

## Running the Code

### 1. Strategy Analysis (Part 1)
Open `strategy_analysis.md` to review strategic analysis, business rules, and implementation roadmap.

### 2. Experimental Notebook (Part 2)
```bash
# Launch Jupyter and open tmp_answers_part2.ipynb
jupyter notebook tmp_answers_part2.ipynb
```

This notebook contains:
- Data loading and profiling with Polars
- Filtering logic for inactive products
- Feature engineering (one-hot encoding, stockout features, price elasticity)
- Parallel processing examples
- Pandas equivalents in comments for reference

### 3. Main Engineering Notebook
```bash
jupyter notebook engineering.ipynb
```

### 4. Production Code
```bash
# Run production code
python production_code.py

# Run tests (if implemented)
python -m pytest tests/

# Import and use functions
python -c "import production_code as pc; help(pc)"
```

## Virtual Environment Management

```bash
# Deactivate virtual environment
deactivate

# Reactivate when returning to project
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Update dependencies
pip install --upgrade -r requirements.txt

# Freeze current environment
pip freeze > requirements_freeze.txt
```

## Key Features

- **Polars-first approach** for efficient data processing
- **Pandas equivalents** documented in code comments
- **Parallel processing** for large-scale batch operations
- **Feature engineering** for demand forecasting (stockout detection, price elasticity)
- **Production-ready** code with error handling and documentation

## Contact
For questions or clarifications, please reach out to Dany Stefan.
