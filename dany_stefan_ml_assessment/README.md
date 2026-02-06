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
├── engineering.ipynb            # Part 2: ML engineering work with Polars (Tasks 4-5)
├── production_code.py           # Part 2: Production-ready forecasting utilities (Task 6)
├── requirements.txt             # Python dependencies
├── presentation.html            # Technical presentation (10-12 slides)
├── data/
│   └── fashion_sample.csv       # Sample data (100 days, 1 product, 1 store)
└── [archived files]             # tmp_answers*.ipynb, tmp_answers.md, etc.
```

## Setup Instructions

### Prerequisites
- Python 3.9+ (tested on Python 3.11)
- pip or pip3

### Installation
```bash
# Navigate to project directory
cd dany_stefan_ml_assessment

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

# Upgrade pip (recommended)
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import polars as pl; import sklearn; print(f'✓ Polars {pl.__version__}'); print(f'✓ scikit-learn {sklearn.__version__}')"
```
[strategy_analysis.md](strategy_analysis.md) to review:
- Strategic analysis and business requirements
- Product qualification rules and filtering logic
- Implementation roadmap and recommendations

### 2. Engineering Notebook (Part 2)
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Launch Jupyter
jupyter notebook engineering.ipynb
```

**Notebook Contents:**
- Data loading and profiling with Polars
- Product qualification and filtering logic
- Feature engineering (lag features, stockout detection, one-hot encoding)
- Gradient Boosting models (scikit-learn, LightGBM)
- Model evaluation (MAE, RMSE, WMAPE)
- Feature importance analysis

**Key Findings:**
- Baseline model (lag features only): WMAPE ~16%
- Custom features model: WMAPE ~10% (37% improvement)
- LightGBM showed best performance with lag + engineered features

### 3. Production Code
```bash
# Import and use production utilities
python -c "from production_code import detect_stockouts, engineer_time_features; help(detect_stockouts)"

# Run in production pipeline
python production_code.py
```

**Available Functions:**
- `detect_stockouts()`: Identify stockout periods
- `engineer_time_features()`: Create time-based features
- Data validation and quality checkshon -m pytest tests/

# Import and use functions
python -c "import production_code as pc; help(pc)"
```macOS/Linux
# venv\Scripts\activate  # Windows

# Update dependencies
pip install --upgrade -r requirements.txt

# List installed packages
pip list

# Freeze current environment (for reproducibility)
pip freeze > requirements_freeze.txt
### Engineering Notebook (engineering.ipynb)
- **Polars-first approach** for efficient data processing
- **Gradient Boosting models** (scikit-learn, LightGBM) for demand forecasting
- **Feature engineering**: lag features, stockout detection, time-based features
- **Model comparison**: Baseline vs. custom features (37% WMAPE improvement)
- **Visualization**: matplotlib/seaborn for EDA and feature importance

### Production Code (production_code.py)
- Type-annotated functions with Polars DataFrames
- Modular utilities for data quality checks and feature engineering
- Designed for integration into production forecasting pipelines
- Documentation and examples for each function

## Technologies Used
- **Polars**: High-performance DataFrame library for data processing
- **scikit-learn**: Machine learning models (LinearRegression, GradientBoostingRegressor)
- **LightGBM**: Gradient boosting framework for best model performance
- **NumPy**: Numerical computing and array operations
- **matplotlib/seaborn**: Data visualization and plotting

## Contact
**Candidate:** Dany Stefan  
**Date:** February 2026   `ModuleNotFoundError: No module named 'polars'`
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: Jupyter kernel not found
```bash
# Install ipykernel in the virtual environment
pip install ipykernel
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
# In Jupyter, select Kernel > Change Kernel > Python (venv)
```

**Issue**: LightGBM installation fails on macOS
```bash
# Install with Homebrew dependencies
brew install libomp
pip install lightgbm

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
