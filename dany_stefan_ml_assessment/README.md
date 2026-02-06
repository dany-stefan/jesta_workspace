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
- Python 3.9+ (tested on Python 3.11 and 3.13)
- pip or pip3

### Installation
```bash
# Navigate to project directory
cd dany_stefan_ml_assessment

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows

# Upgrade pip (recommended)
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import polars as pl; import sklearn; print(f'✓ Polars {pl.__version__}'); print(f'✓ scikit-learn {sklearn.__version__}')"
```

## Usage

### 1. Strategic Analysis (Part 1)
Review [strategy_analysis.md](strategy_analysis.md) for:
- Strategic analysis and business requirements
- Product qualification rules and filtering logic
- Implementation roadmap and recommendations

### 2. Engineering Notebook (Part 2)
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Launch Jupyter
jupyter notebook engineering.ipynb
```

**How to Run:**
1. Open the notebook in Jupyter
2. Run cells sequentially: **Cell > Run All** or execute cells one by one
3. **Note:** Cells 50-51 use LightGBM (optional - can skip if not installed)
4. All other 31 code cells work without LightGBM

**Notebook Contents:**
- Data loading and profiling with Polars ✅
- Product qualification and filtering logic ✅
- Feature engineering (lag features, stockout detection, time features) ✅
- Gradient Boosting models with scikit-learn ✅
- Model evaluation (MAE, RMSE, WMAPE) ✅
- Feature importance analysis ✅
- *(Optional)* LightGBM comparison (cells 50-51, requires separate setup)

**Key Findings:**
- Baseline model (lag features only): WMAPE ~16%
- Custom features model: WMAPE ~10% (37% improvement)
- scikit-learn GradientBoostingRegressor shows strong performance

### 3. Production Code Templates (Task 6)

**⚠️ Note:** `production_code.py` contains **function templates/stubs** designed as blueprints for production integration. For working implementations, see `engineering.ipynb`.

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Import the module (templates can be imported)
python -c "import production_code; print('✓ Import successful')"

# View function templates and documentation
python -c "import production_code as pc; help(pc)"
python -c "from production_code import detect_stockouts; help(detect_stockouts)"
```

**Template Functions:**
- `detect_stockouts()`: Template for identifying stockout periods
- `engineer_time_features()`: Template for time-based feature engineering
- `engineer_price_features()`: Template for pricing features
- `engineer_inventory_features()`: Template for inventory features

**To see working implementations:** Open and run `engineering.ipynb`.

## Technologies Used
- **Polars**: High-performance DataFrame library for data processing
- **scikit-learn**: Machine learning models (GradientBoostingRegressor)
- **NumPy/Pandas**: Numerical computing and data analysis
- **matplotlib/seaborn**: Data visualization and plotting
- **(Optional) LightGBM**: Advanced gradient boosting (requires extra setup on macOS)

## Key Features

### Engineering Notebook (engineering.ipynb)
- **Polars-first approach** for efficient data processing
- **Gradient Boosting models** (scikit-learn, LightGBM) for demand forecasting
- **Feature engineering**: lag features, stockout detection, time-based features
- **Model comparison**: Baseline vs. custom features (37% WMAPE improvement)
- **Visualization**: matplotlib/seaborn for EDA and feature importance

### Production Code Templates (production_code.py)
- Function templates with type annotations for Polars DataFrames
- Blueprint for data quality checks and feature engineering utilities
- Designed as starting point for production forecasting pipelines
- See `engineering.ipynb` for working implementations

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'polars'`
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Note: .venv not venv
pip install -r requirements.txt
```

**Issue**: Jupyter kernel not found
```bash
# Install ipykernel in the virtual environment
pip install ipykernel
python -m ipykernel install --user --name=.venv --display-name "Python (.venv)"
# In Jupyter, select Kernel > Change Kernel > Python (.venv)
```

**Issue**: `OSError: LightGBM failed to load libomp` (macOS)
```bash
# LightGBM is optional - you can skip cells 50-51 in notebook
# If you want it, install libomp first:
brew install libomp
pip install lightgbm

# Then restart Jupyter kernel:
# In Jupyter: Kernel > Restart Kernel
```

**Issue**: Notebook cells fail
```bash
# If cells 50-51 fail (LightGBM), you can skip them
# All other 31 code cells should work fine
# Try running cells one by one to identify issues
```

**Issue**: production_code.py functions return None
```bash
# This is expected - production_code.py contains function templates
# For working implementations, see engineering.ipynb
```

## Maintenance

```bash
# Reactivate when returning to project
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Update dependencies
pip install --upgrade -r requirements.txt

# Freeze current environment
pip freeze > requirements_freeze.txt
```
## Quick Start (For Reviewers)

```bash
# 1. Setup (1-2 minutes)
cd dany_stefan_ml_assessment
python3 -m venv .venv
source .venv/bin/activate
pip install polars numpy pandas scikit-learn matplotlib seaborn jupyter

# 2. Run notebook (5-10 minutes)
jupyter notebook engineering.ipynb
# In Jupyter: Cell > Run All (skip LightGBM errors if they appear)

# 3. Test imports
python -c "import production_code; print('✓ Production code imports successfully')"
```

## Notes for Reproducibility

✅ **Tested on:**
- macOS with Python 3.11 and 3.13
- Virtual environment: `.venv`
- Core packages work without LightGBM

✅ **What works out of the box:**
- Data loading and exploration (Polars)
- Feature engineering (31/33 notebook cells)
- scikit-learn models
- Visualization
- production_code.py imports (templates)

⚠️ **Optional (can skip):**
- LightGBM (cells 50-51 in notebook)
- Requires `brew install libomp` on macOS
## Contact
For questions or clarifications, please reach out to Dany Stefan.
