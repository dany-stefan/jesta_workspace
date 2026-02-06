# Senior ML Engineer Technical Assessment
**Candidate:** Dany Stefan  
**Position:** Senior MLOps Engineer  
**Date:** February 2026

## Overview
This assessment demonstrates ML engineering capabilities for demand forecasting in retail/fashion, including strategic analysis, feature engineering, and production-ready code.

## 🚀 Quick Start

**Get running in 3 steps:**

```bash
# 1. Setup environment
cd dany_stefan_ml_assessment
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux (.venv\Scripts\activate on Windows)
pip install -r requirements.txt

# 2. Run production code (CLI tool)
python production_code.py
# Output: Detects stockouts in fashion_sample.csv data

# 3. Run engineering notebook
jupyter notebook engineering.ipynb
# Then in Jupyter: Cell > Run All (or Shift+Enter through cells)
```

**That's it!** Both files are fully executable and portable.

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
- **Minimum 100MB free disk space** (for dependencies)
- **No GPU required** - Runs on CPU

### Execution Requirements

Both components are **portable and self-contained**:

| Component | Requires | Optional | Runs On |
|-----------|----------|----------|----------|
| production_code.py | Polars, NumPy | - | Any OS with Python 3.9+ |
| engineering.ipynb | Polars, scikit-learn, matplotlib | LightGBM | Jupyter/VS Code |
| Data | data/fashion_sample.csv | Custom CSV | Any filesystem |

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

### 3. Production Code (Task 6)

`production_code.py` is a **portable, executable script** with working stockout detection and command-line interface.

#### Quick Run
```bash
# Basic execution (uses data/fashion_sample.csv, runs tests)
python production_code.py
```

#### Advanced Options
```bash
# Custom data file
python production_code.py --data-file path/to/your/data.csv

# Different lookback period (default: 7 days)
python production_code.py --lookback-days 14

# Skip test functions
python production_code.py --skip-tests

# See all options
python production_code.py --help
```

**Features:**
- ✅ **Fully executable** - Works standalone with validation and error handling
- ✅ **Command-line arguments** - Flexible input parameters
- ✅ **Input validation** - Checks file paths, data types, parameter ranges
- ✅ **Error handling** - Graceful failures with clear error messages
- ✅ **Portable** - Can be run on any system with Python 3.9+ and dependencies

**Working Functions:**
- `detect_stockouts()`: Identifies stockout periods (inventory=0, recent sales>0)
  - Input: DataFrame with date, sales, inventory columns
  - Output: DataFrame with `is_stockout` and `recent_sales` columns
  - Configurable lookback window (default: 7 days)

**Import as Module:**
```python
import polars as pl
from production_code import detect_stockouts

# Load your data
df = pl.read_csv("your_data.csv")

# Detect stockouts
result = detect_stockouts(df, lookback_days=7)
stockouts = result.filter(pl.col("is_stockout"))
```

## Portability & Execution

### ✅ Portable Components

Both the notebook and production code are designed to be **fully portable** and executable:

**1. Notebook (engineering.ipynb)**
- ✅ Self-contained analysis with markdown documentation
- ✅ Can be run cell-by-cell or all at once
- ✅ Works with Jupyter, VS Code, or JupyterLab
- ✅ Requires only core dependencies (Polars, scikit-learn, matplotlib)
- ⚠️ Optional: LightGBM for cells 50-51 (can skip)

**2. Production Script (production_code.py)**
- ✅ Standalone executable with CLI interface
- ✅ Works with default data or custom CSV files
- ✅ Input validation and error handling
- ✅ Can be imported as a Python module
- ✅ Cross-platform (macOS, Linux, Windows)

**3. Data**
- ✅ Sample data included: `data/fashion_sample.csv`
- ✅ CSV format (100 rows, 9 columns)
- ✅ Can be replaced with your own data

### 🚀 Quick Execution Examples

**Option 1: Run from terminal**
```bash
# Production script (takes ~1 second)
python production_code.py
# Expected output: 32 stockout periods detected, test results

# Execute notebook from command line (takes ~2-3 minutes)
jupyter nbconvert --to notebook --execute engineering.ipynb --output engineering_executed.ipynb
```

**Option 2: Interactive execution**
```bash
# Open notebook in Jupyter
jupyter notebook engineering.ipynb
# Then: Cell > Run All (or run cells individually)

# Open notebook in VS Code
code engineering.ipynb
# Click "Run All" button in toolbar
```

**Expected Results:**
- `production_code.py`: Prints 32 stockout periods, passes all tests
- `engineering.ipynb`: Completes all cells, shows model achieving 10.41% WMAPE (37% improvement)

## Technologies Used
- **Polars**: High-performance DataFrame library for data processing
- **scikit-learn**: Machine learning models (GradientBoostingRegressor)
- **NumPy/Pandas**: Numerical computing and data analysis
- **matplotlib/seaborn**: Data visualization and plotting
- **(Optional) LightGBM**: Advanced gradient boosting (requires extra setup on macOS)

## Key Features

### Engineering Notebook (engineering.ipynb)
- ✅ **Portable & Executable** - Run cell-by-cell or all at once
- ✅ **Polars-first approach** for efficient data processing
- ✅ **Gradient Boosting models** (scikit-learn) for demand forecasting
- ✅ **Feature engineering**: lag features, stockout detection, time-based features
- ✅ **Model comparison**: Baseline vs. custom features (37% WMAPE improvement)
- ✅ **Visualization**: matplotlib/seaborn for EDA and feature importance
- ✅ **94% runnable** - 31 out of 33 cells work without LightGBM

### Production Code (production_code.py)
- ✅ **Fully Executable** - Working CLI tool with stockout detection
- ✅ **Command-line Interface** - Flexible arguments (--data-file, --lookback-days)
- ✅ **Input Validation** - Type checking, file existence, parameter validation
- ✅ **Error Handling** - Try-catch blocks with clear error messages
- ✅ **Module Import** - Can be imported and used in other scripts
- ✅ **Type Annotations** - Full type hints for Polars DataFrames
- ✅ **Production Ready** - Designed for integration into forecasting pipelines

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

**Issue**: production_code.py gives file not found error
```bash
# Make sure you're in the correct directory
cd dany_stefan_ml_assessment
python production_code.py

# Or use absolute path
python /full/path/to/production_code.py --data-file /full/path/to/data.csv
```

**Issue**: Notebook won't execute all cells
```bash
# Execute from command line
jupyter nbconvert --to notebook --execute engineering.ipynb

# Or in Jupyter interface:
# 1. Kernel > Restart Kernel
# 2. Cell > Run All
# 3. Wait for completion (may take 2-3 minutes)
```

**Issue**: Command-line arguments not working
```bash
# Check help to see available options
python production_code.py --help

# Make sure to use correct syntax
python production_code.py --data-file="data/fashion_sample.csv" --lookback-days=14
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
