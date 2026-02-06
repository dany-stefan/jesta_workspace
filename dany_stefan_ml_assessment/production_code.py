"""
Production-ready forecasting utilities for fashion retail demand.

This module provides data quality checks, feature engineering, and
forecasting functions designed for production use with Polars DataFrames.

Author: Dany Stefan
Date: February 2026
"""

import polars as pl
from typing import Optional, List, Dict, Any
import argparse
import sys
from pathlib import Path


# ============================================================================
# Data Quality & Validation Functions
# ============================================================================

def detect_stockouts(
    df: pl.DataFrame,
    lookback_days: int = 7
) -> pl.DataFrame:
    """
    Detect periods where inventory=0 but recent sales>0.

    Args:
        df: Sales data with columns [date (datetime), sales(int), inventory(int)]
        lookback_days: Days to look back for recent sales

    Returns:
        DataFrame with added column 'is_stockout' for result
        Intermediate results: 'recent_sales' column added

    Example:
        >>> df = detect_stockouts(sales_df, lookback_days=7)
        >>> df.filter(pl.col('is_stockout'))
        >>> df = pl.DataFrame({
            ...     "date": ["2026-01-01", "2026-01-02"],
            ...     "sales": [5, 0],
            ...     "inventory": [1, 0]
            ... })
    """
    assert lookback_days > 0, f"lookback_days must be positive, got {lookback_days}"
    min_rows = lookback_days  # At least lookback_days worth of data
    if df.height < min_rows:
        print(f"Warning: DataFrame has only {df.height} rows, minimum {min_rows} recommended")
    
    ## Input validation
    # Ensure required columns are present
    required_cols = {"date", "sales", "inventory"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"Input DataFrame must contain columns: {required_cols}")
    # Ensure correct data types
    try:
        df = df.with_columns([
            pl.col("date").cast(pl.Date),
            pl.col("sales").cast(pl.Int32),
            pl.col("inventory").cast(pl.Int32)
        ])
    except Exception as e:
        raise TypeError(
            f"Failed to cast columns to required types. "
            f"Expected: date (Date), sales (Int32), inventory (Int32). "
            f"Error: {str(e)}"
        )

    # Sort by date to ensure correct rolling calculations
    df = df.sort("date")

    # Calculate rolling sum of sales over the lookback period
    df = df.with_columns([
        pl.col("sales")
        .rolling_sum(window_size=lookback_days, min_samples=1)
        .alias("recent_sales")
    ])

    # Condition given recent sales, get stockouts
    df = df.with_columns([
        ((pl.col("inventory") == 0) & (pl.col("recent_sales") > 0))
        .alias("is_stockout")
    ])

    
    return df


# ============================================================================
# Test Functions
# ============================================================================

def test_stockouts_basic():
    """Test clear stockout case"""
    print("BASIC test running")
    df = pl.DataFrame({
        "date": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "sales": [5, 3, 0],
        "inventory": [10, 0, 0],
    })
    result = detect_stockouts(df, lookback_days=2)  # Function call
    
    is_stockout_list = result.select(pl.col("is_stockout")).to_series().to_list()
    expected = [False, True, True]
    if is_stockout_list != expected:
        raise AssertionError(f"is_stockout values do not match expected.\nGot: {is_stockout_list}\nExpected: {expected}")


def test_stockouts_edge_cases():
    """Test no data, missing columns, etc"""
    print("EDGE CASES test running")
    # Edge case 1: Empty DataFrame should return empty result
    df_empty = pl.DataFrame({
        "date": [],
        "sales": [],
        "inventory": [],
    })
    try:
        result_empty = detect_stockouts(df_empty, lookback_days=1)  # Function call
        if result_empty.height != 0:
            raise AssertionError(f"Expected empty result (height=0) for empty input, got {result_empty.height}")
        print(f"Empty DataFrame test passed: returned {result_empty.height} rows")
    except Exception as e:
        print(f"Empty DataFrame test failed: {e}")


    # Edge case 2: Missing columns should raise ValueError
    df_missing = pl.DataFrame({
        "date": ["2026-01-01"],
        "sales": [1],
        #"inventory": [],
    })
    try:
        detect_stockouts(df_missing)    # Function call
        assert False, "Expected ValueError for missing columns"
    except ValueError as e:
        print(f"Caught expected ValueError: {e}")


# ============================================================================
# Main execution for testing
# ============================================================================

if __name__ == "__main__":
     # Check if file exists
    data_path = Path("./data/fashion_sample.csv")   # Path can be command line args
    if not data_path.exists():
        print(f"Error: Data file not found at {data_path}")
        sys.exit(1)

    # Load the data
    df = pl.read_csv(str(data_path))

    # Convert date columns to proper types and extract date features
    '''
    df = df.with_columns([
        pl.col("date").str.to_date().alias("date"),
        pl.col("launch_date").str.to_date().alias("launch_date")
    ])
    '''

    # Add day_number column (Day 1, Day 2, ..., Day N)
    # this can be a function too (reusable)
    df = df.with_columns([
        (pl.col("date").rank(method="dense") - 1 + 1).cast(pl.Int32).alias("day_number")
    ])

    # Detect stockouts
    detected_df = detect_stockouts(df, lookback_days=4)
    print(detected_df.filter(pl.col("is_stockout")))

    print("Running production code tests...")
    
    # Run all tests
    test_stockouts_basic()
    test_stockouts_edge_cases()
    
    print("All tests completed!")
