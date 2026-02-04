"""
Unit tests for production_code.py

Tests cover stockout detection functionality including:
- Basic stockout detection
- Edge cases (no stockouts, continuous stockouts)
- Data validation
- Lost sales calculation
- Pattern analysis
"""

import polars as pl
import pytest
from production_code import detect_stockouts, analyze_stockout_patterns


class TestDetectStockouts:
    """Test cases for detect_stockouts function"""
    
    def test_basic_stockout_detection(self):
        """Test detection of a simple stockout event"""
        # Create test data with a stockout
        data = {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "style": ["STYLE-A"] * 5,
            "site": ["STORE-1"] * 5,
            "inventory": [100, 50, 0, 0, 100],  # Stockout on days 3-4
            "sales": [50, 50, 0, 0, 10]
        }
        df = pl.DataFrame(data)
        
        result = detect_stockouts(df)
        
        # Should detect one stockout event
        assert len(result) == 1
        assert result["stockout_days"][0] == 2
        assert result["style"][0] == "STYLE-A"
        assert result["site"][0] == "STORE-1"
    
    def test_no_stockouts(self):
        """Test with data that has no stockouts"""
        data = {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "style": ["STYLE-A"] * 3,
            "site": ["STORE-1"] * 3,
            "inventory": [100, 80, 60],  # Never reaches zero
            "sales": [20, 20, 20]
        }
        df = pl.DataFrame(data)
        
        result = detect_stockouts(df)
        
        # Should find no stockouts
        assert len(result) == 0
    
    def test_multiple_stockout_periods(self):
        """Test detection of multiple separate stockout periods"""
        data = {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", 
                     "2024-01-05", "2024-01-06", "2024-01-07"],
            "style": ["STYLE-A"] * 7,
            "site": ["STORE-1"] * 7,
            "inventory": [100, 0, 0, 50, 0, 0, 100],  # Two stockout periods
            "sales": [100, 0, 0, 50, 0, 0, 10]
        }
        df = pl.DataFrame(data)
        
        result = detect_stockouts(df)
        
        # Should detect two separate stockout events
        assert len(result) == 2
        assert all(days in [2, 2] for days in result["stockout_days"])
    
    def test_multiple_groups(self):
        """Test stockout detection across multiple style/site combinations"""
        data = {
            "date": ["2024-01-01", "2024-01-02", "2024-01-01", "2024-01-02"],
            "style": ["STYLE-A", "STYLE-A", "STYLE-B", "STYLE-B"],
            "site": ["STORE-1", "STORE-1", "STORE-1", "STORE-1"],
            "inventory": [100, 0, 0, 0],  # STYLE-A has 1 day, STYLE-B has 2 days
            "sales": [100, 0, 0, 0]
        }
        df = pl.DataFrame(data)
        
        result = detect_stockouts(df)
        
        # Should detect stockouts for both styles
        assert len(result) == 2
        assert set(result["style"]) == {"STYLE-A", "STYLE-B"}
    
    def test_lost_sales_calculation(self):
        """Test that lost sales opportunity is calculated correctly"""
        data = {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "style": ["STYLE-A"] * 5,
            "site": ["STORE-1"] * 5,
            "inventory": [100, 80, 60, 0, 0],  # Stockout on days 4-5
            "sales": [20, 20, 20, 0, 0]  # Average = 20
        }
        df = pl.DataFrame(data)
        
        result = detect_stockouts(df)
        
        # Lost sales should be approximately 20 * 2 = 40
        assert len(result) == 1
        assert result["lost_sales_opportunity"][0] == pytest.approx(20.0 * 2, rel=0.1)
    
    def test_missing_sales_values(self):
        """Test handling of missing sales values"""
        data = {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "style": ["STYLE-A"] * 3,
            "site": ["STORE-1"] * 3,
            "inventory": [100, 50, 0],
            "sales": [50, None, None]  # Missing sales during stockout
        }
        df = pl.DataFrame(data)
        
        # Should handle without error
        result = detect_stockouts(df)
        assert len(result) == 1
    
    def test_custom_column_names(self):
        """Test using custom column names"""
        data = {
            "order_date": ["2024-01-01", "2024-01-02"],
            "product": ["PROD-A"] * 2,
            "location": ["LOC-1"] * 2,
            "stock": [100, 0],
            "units_sold": [100, 0]
        }
        df = pl.DataFrame(data)
        
        result = detect_stockouts(
            df,
            group_cols=["product", "location"],
            date_col="order_date",
            inventory_col="stock",
            sales_col="units_sold"
        )
        
        assert len(result) == 1
        assert "product" in result.columns
        assert "location" in result.columns
    
    def test_missing_columns_error(self):
        """Test that missing required columns raises an error"""
        data = {
            "date": ["2024-01-01"],
            "style": ["STYLE-A"],
            # Missing 'site', 'inventory', 'sales'
        }
        df = pl.DataFrame(data)
        
        with pytest.raises(ValueError, match="Missing required columns"):
            detect_stockouts(df)
    
    def test_date_string_conversion(self):
        """Test that date strings are properly converted"""
        data = {
            "date": ["2024-01-01", "2024-01-02"],  # String dates
            "style": ["STYLE-A"] * 2,
            "site": ["STORE-1"] * 2,
            "inventory": [100, 0],
            "sales": [100, 0]
        }
        df = pl.DataFrame(data)
        
        # Should handle string dates
        result = detect_stockouts(df)
        assert len(result) == 1
    
    def test_continuous_stockout(self):
        """Test a long continuous stockout period"""
        dates = [f"2024-01-{i:02d}" for i in range(1, 11)]
        data = {
            "date": dates,
            "style": ["STYLE-A"] * 10,
            "site": ["STORE-1"] * 10,
            "inventory": [100] + [0] * 9,  # 9-day stockout
            "sales": [100] + [0] * 9
        }
        df = pl.DataFrame(data)
        
        result = detect_stockouts(df)
        
        # Should detect one long stockout
        assert len(result) == 1
        assert result["stockout_days"][0] == 9


class TestAnalyzeStockoutPatterns:
    """Test cases for analyze_stockout_patterns function"""
    
    def test_basic_pattern_analysis(self):
        """Test basic pattern analysis"""
        stockouts_data = {
            "style": ["STYLE-A", "STYLE-B"],
            "site": ["STORE-1", "STORE-1"],
            "stockout_start": ["2024-01-01", "2024-01-02"],
            "stockout_end": ["2024-01-02", "2024-01-03"],
            "stockout_days": [2, 2],
            "lost_sales_opportunity": [50.0, 30.0]
        }
        df = pl.DataFrame(stockouts_data)
        
        result = analyze_stockout_patterns(df)
        
        assert result["total_stockout_events"] == 2
        assert result["total_lost_sales"] == 80.0
        assert result["avg_stockout_duration"] == 2.0
        assert len(result["worst_styles"]) == 2
        assert len(result["worst_sites"]) == 1
    
    def test_empty_stockouts(self):
        """Test pattern analysis with no stockouts"""
        df = pl.DataFrame({
            "style": [],
            "site": [],
            "stockout_start": [],
            "stockout_end": [],
            "stockout_days": [],
            "lost_sales_opportunity": []
        })
        
        result = analyze_stockout_patterns(df)
        
        assert result["total_stockout_events"] == 0
        assert result["total_lost_sales"] == 0.0
        assert result["avg_stockout_duration"] == 0.0
    
    def test_min_lost_sales_filter(self):
        """Test filtering by minimum lost sales threshold"""
        stockouts_data = {
            "style": ["STYLE-A", "STYLE-B", "STYLE-C"],
            "site": ["STORE-1"] * 3,
            "stockout_start": ["2024-01-01"] * 3,
            "stockout_end": ["2024-01-02"] * 3,
            "stockout_days": [1, 1, 1],
            "lost_sales_opportunity": [100.0, 5.0, 50.0]  # One below threshold
        }
        df = pl.DataFrame(stockouts_data)
        
        result = analyze_stockout_patterns(df, min_lost_sales=10.0)
        
        # Should only count stockouts with lost_sales >= 10.0
        assert result["total_stockout_events"] == 2
        assert result["total_lost_sales"] == 150.0


class TestIntegrationWithSampleData:
    """Integration tests using the provided sample data"""
    
    def test_with_fashion_sample_csv(self):
        """Test with the actual fashion_sample.csv file"""
        try:
            df = pl.read_csv("fashion_sample.csv")
            
            # Run stockout detection
            stockouts = detect_stockouts(df)
            
            # Should detect at least one stockout (based on the sample data preview)
            assert len(stockouts) >= 1
            
            # Verify structure
            assert "stockout_start" in stockouts.columns
            assert "stockout_end" in stockouts.columns
            assert "stockout_days" in stockouts.columns
            assert "lost_sales_opportunity" in stockouts.columns
            
            # Run pattern analysis
            patterns = analyze_stockout_patterns(stockouts)
            
            assert patterns["total_stockout_events"] >= 0
            assert isinstance(patterns["total_lost_sales"], float)
            
        except FileNotFoundError:
            pytest.skip("fashion_sample.csv not found")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
