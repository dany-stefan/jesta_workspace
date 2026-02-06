"""
Production-ready forecasting utilities for fashion retail demand.

This module provides data quality checks, feature engineering, and
forecasting functions designed for production use with Polars DataFrames.

Author: Dany Stefan
Date: February 2026
"""

import polars as pl
from typing import Optional, List, Dict, Any


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
    """
    ## Input validation
    # Ensure required columns are present
    required_cols = {"date", "sales", "inventory"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"Input DataFrame must contain columns: {required_cols}")
    # Ensure correct data types
    df = df.with_columns(["date", "sales", "inventory"].map(
        lambda col: pl.col(col).cast(pl.Int32) if col != "date" else pl.col(col).cast(pl.Date)
    ))

    # Sort by date to ensure correct rolling calculations
    df = df.sort("date")

    # Calculate rolling sum of sales over the lookback period
    df = df.with_columns([
        pl.col("sales")
        .rolling_sum(window_size=lookback_days, min_periods=1)
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
    # TODO: Implementation
    pass


def test_stockouts_edge_cases():
    """Test no data, missing columns, etc"""
    # TODO: Implementation
    pass


# ============================================================================
# Main execution for testing
# ============================================================================

if __name__ == "__main__":
    # Load the data
    df = pl.read_csv("data/fashion_sample.csv")

    # Convert date columns to proper types and extract date features
    df = df.with_columns([
        pl.col("date").str.to_date().alias("date"),
        pl.col("launch_date").str.to_date().alias("launch_date")
    ])

    # Add day_number column (Day 1, Day 2, ..., Day N)
    # this can be a function too (reusable)
    df = df.with_columns([
        (pl.col("date").rank(method="dense") - 1 + 1).cast(pl.Int32).alias("day_number")
    ])

    # Detect stockouts
    detected_df = detect_stockouts(df, lookback_days=7)
    print(detected_df.filter(pl.col("is_stockout")))

    print("Running production code tests...")
    
    # Run all tests
    test_stockouts_basic()
    test_stockouts_edge_cases()
    
    print("All tests completed!")
