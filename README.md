# Jesta Technical Assessment - Senior MLOps Engineer

This repository contains my implementation for the Jesta technical assessment, focusing on inventory management and stockout detection for fashion retail.

## Project Structure

```
.
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── production_code.py                 # Main implementation code
├── test_production_code.py           # Unit tests
├── part1_strategy/                   # Strategy and architecture documents
│   └── root_cause_memo.md           # Root cause analysis
├── fashion_sample.csv                # Sample sales data
└── 2026-01-30-take home technical test for Senior ML Engineer v2.pdf
```

## Setup

### Installation

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest test_production_code.py -v
```

## Part 1: Strategy & Architecture

The `part1_strategy/` directory contains the root cause analysis memo addressing:
- Problems with the existing forecasting system
- Realistic roadmap for improvements
- Strategic recommendations

## Part 2: Code Implementation

### Stockout Detection

The main functionality is implemented in `production_code.py`, which provides:
- `detect_stockouts()`: Function to identify stockout events in sales data
- Clean, maintainable code using Polars for data manipulation
- Comprehensive error handling and edge case management

### Key Features

- **Polars-based**: Uses Polars library for efficient data manipulation
- **Production-ready**: Clean, well-documented code following best practices
- **Tested**: Comprehensive unit tests ensuring reliability
- **Maintainable**: Clear structure and documentation for future development

## Usage

```python
import polars as pl
from production_code import detect_stockouts

# Load sales data
df = pl.read_csv("fashion_sample.csv")

# Detect stockouts
stockouts = detect_stockouts(df)

# Analyze results
print(f"Found {len(stockouts)} stockout events")
```

## About

This implementation demonstrates:
- Strong understanding of retail inventory challenges
- Clean, maintainable code practices
- Thoughtful feature engineering
- Production-ready software development
- Clear communication and documentation
