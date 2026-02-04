"""
Production code for Jesta Technical Assessment - Stockout Detection

This module provides functionality to detect stockout events in retail sales data,
helping identify lost sales opportunities due to inventory depletion.

Author: Candidate for Senior MLOps Engineer Position
Date: February 2026
"""

import polars as pl
from typing import Optional
from datetime import datetime


def detect_stockouts(
    df: pl.DataFrame,
    group_cols: Optional[list[str]] = None,
    date_col: str = "date",
    inventory_col: str = "inventory",
    sales_col: str = "sales"
) -> pl.DataFrame:
    """
    Detect stockout events in sales data.
    
    A stockout is identified when:
    1. Inventory reaches zero
    2. There's a subsequent period where inventory remains at zero
    3. Sales are either zero or missing during the stockout period
    
    Args:
        df: Input DataFrame containing sales and inventory data
        group_cols: Columns to group by (e.g., ['style', 'site'])
                   If None, defaults to ['style', 'site']
        date_col: Name of the date column
        inventory_col: Name of the inventory column
        sales_col: Name of the sales column
    
    Returns:
        DataFrame with stockout events including:
        - All original grouping columns
        - stockout_start: First date when inventory reached zero
        - stockout_end: Last consecutive date with zero inventory
        - stockout_days: Number of days in stockout
        - lost_sales_opportunity: Estimated lost sales based on pre-stockout average
        
    Example:
        >>> df = pl.read_csv("fashion_sample.csv")
        >>> stockouts = detect_stockouts(df)
        >>> print(f"Found {len(stockouts)} stockout events")
    
    Notes:
        - Assumes data is sorted by date within groups
        - Missing sales values during stockout are treated as lost opportunities
        - Pre-stockout average is calculated from the 7 days before stockout
    """
    if group_cols is None:
        group_cols = ["style", "site"]
    
    # Validate required columns exist
    required_cols = group_cols + [date_col, inventory_col, sales_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Ensure date column is datetime type
    if df[date_col].dtype != pl.Date and df[date_col].dtype != pl.Datetime:
        df = df.with_columns(pl.col(date_col).str.to_date())
    
    # Sort by group columns and date
    df = df.sort(group_cols + [date_col])
    
    # Identify stockout periods (inventory = 0)
    df = df.with_columns([
        (pl.col(inventory_col) == 0).alias("is_stockout")
    ])
    
    # Create a run identifier for consecutive stockout days
    # This helps group consecutive stockout periods together
    df = df.with_columns([
        # Shift is_stockout to identify transitions
        pl.col("is_stockout").shift(1).over(group_cols).alias("prev_stockout"),
    ])
    
    # Mark start of new stockout periods
    df = df.with_columns([
        (
            pl.col("is_stockout") & 
            (pl.col("prev_stockout").is_null() | ~pl.col("prev_stockout"))
        ).alias("stockout_start_marker")
    ])
    
    # Create stockout run ID by cumulative sum of start markers
    df = df.with_columns([
        pl.col("stockout_start_marker")
        .cum_sum()
        .over(group_cols)
        .alias("stockout_run_id")
    ])
    
    # Filter to only stockout periods
    stockout_periods = df.filter(pl.col("is_stockout"))
    
    if len(stockout_periods) == 0:
        # No stockouts found, return empty DataFrame with expected schema
        return pl.DataFrame({
            **{col: [] for col in group_cols},
            "stockout_start": [],
            "stockout_end": [],
            "stockout_days": [],
            "lost_sales_opportunity": []
        })
    
    # Aggregate stockout periods
    stockouts = (
        stockout_periods
        .group_by(group_cols + ["stockout_run_id"])
        .agg([
            pl.col(date_col).min().alias("stockout_start"),
            pl.col(date_col).max().alias("stockout_end"),
            pl.col(date_col).count().alias("stockout_days"),
        ])
    )
    
    # Calculate lost sales opportunity
    # For each stockout, look at the 7 days before to estimate daily demand
    stockouts_with_lost_sales = []
    
    for stockout_row in stockouts.iter_rows(named=True):
        # Build filter for this specific group
        group_filter = pl.lit(True)
        for col in group_cols:
            group_filter = group_filter & (pl.col(col) == stockout_row[col])
        
        # Get data for this group before stockout
        pre_stockout_data = df.filter(
            group_filter &
            (pl.col(date_col) < stockout_row["stockout_start"]) &
            (pl.col(inventory_col) > 0)  # Only consider days with inventory
        ).tail(7)  # Last 7 days before stockout
        
        # Calculate average daily sales (excluding null values)
        if len(pre_stockout_data) > 0:
            avg_daily_sales = (
                pre_stockout_data[sales_col]
                .drop_nulls()
                .mean()
            )
            if avg_daily_sales is None:
                avg_daily_sales = 0.0
        else:
            avg_daily_sales = 0.0
        
        # Estimate lost sales
        lost_sales = avg_daily_sales * stockout_row["stockout_days"]
        
        # Add to results
        result_row = {**stockout_row, "lost_sales_opportunity": lost_sales}
        stockouts_with_lost_sales.append(result_row)
    
    # Convert back to DataFrame
    result_df = pl.DataFrame(stockouts_with_lost_sales)
    
    # Drop the internal stockout_run_id column
    result_df = result_df.drop("stockout_run_id")
    
    return result_df


def analyze_stockout_patterns(
    stockouts_df: pl.DataFrame,
    min_lost_sales: float = 10.0
) -> dict:
    """
    Analyze patterns in stockout events to identify high-impact issues.
    
    Args:
        stockouts_df: DataFrame from detect_stockouts()
        min_lost_sales: Minimum lost sales to consider significant
    
    Returns:
        Dictionary with analysis results including:
        - total_stockout_events: Total number of stockout events
        - total_lost_sales: Sum of all lost sales opportunities
        - avg_stockout_duration: Average duration of stockout events
        - worst_styles: Top styles by lost sales
        - worst_sites: Top sites by lost sales
    """
    if len(stockouts_df) == 0:
        return {
            "total_stockout_events": 0,
            "total_lost_sales": 0.0,
            "avg_stockout_duration": 0.0,
            "worst_styles": [],
            "worst_sites": []
        }
    
    # Filter to significant stockouts
    significant = stockouts_df.filter(
        pl.col("lost_sales_opportunity") >= min_lost_sales
    )
    
    total_events = len(significant)
    total_lost_sales = significant["lost_sales_opportunity"].sum()
    avg_duration = significant["stockout_days"].mean()
    
    # Aggregate by style
    if "style" in significant.columns:
        worst_styles = (
            significant
            .group_by("style")
            .agg([
                pl.col("lost_sales_opportunity").sum().alias("total_lost_sales"),
                pl.col("stockout_days").sum().alias("total_stockout_days")
            ])
            .sort("total_lost_sales", descending=True)
            .head(10)
        )
        worst_styles_list = worst_styles.to_dicts()
    else:
        worst_styles_list = []
    
    # Aggregate by site
    if "site" in significant.columns:
        worst_sites = (
            significant
            .group_by("site")
            .agg([
                pl.col("lost_sales_opportunity").sum().alias("total_lost_sales"),
                pl.col("stockout_days").sum().alias("total_stockout_days")
            ])
            .sort("total_lost_sales", descending=True)
            .head(10)
        )
        worst_sites_list = worst_sites.to_dicts()
    else:
        worst_sites_list = []
    
    return {
        "total_stockout_events": total_events,
        "total_lost_sales": float(total_lost_sales) if total_lost_sales else 0.0,
        "avg_stockout_duration": float(avg_duration) if avg_duration else 0.0,
        "worst_styles": worst_styles_list,
        "worst_sites": worst_sites_list
    }
