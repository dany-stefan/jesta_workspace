"""
Demo script showcasing the stockout detection functionality

This script demonstrates:
1. Loading sales data
2. Detecting stockout events
3. Analyzing stockout patterns
4. Visualizing key insights
"""

import polars as pl
from production_code import detect_stockouts, analyze_stockout_patterns


def main():
    print("=" * 80)
    print("JESTA TECHNICAL ASSESSMENT - STOCKOUT DETECTION DEMO")
    print("=" * 80)
    print()
    
    # Load the sample data
    print("1. Loading sales data from fashion_sample.csv...")
    df = pl.read_csv("fashion_sample.csv")
    print(f"   ✓ Loaded {len(df)} rows of sales data")
    print(f"   ✓ Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   ✓ Unique styles: {df['style'].n_unique()}")
    print(f"   ✓ Unique sites: {df['site'].n_unique()}")
    print()
    
    # Show a sample of the data
    print("2. Sample of the data:")
    print(df.head(10).select(["date", "style", "site", "sales", "inventory"]))
    print()
    
    # Detect stockouts
    print("3. Detecting stockout events...")
    stockouts = detect_stockouts(df)
    print(f"   ✓ Found {len(stockouts)} stockout events")
    print()
    
    if len(stockouts) > 0:
        print("4. Stockout Details:")
        print(stockouts)
        print()
        
        # Analyze patterns
        print("5. Pattern Analysis:")
        patterns = analyze_stockout_patterns(stockouts)
        
        print(f"\n   Key Metrics:")
        print(f"   • Total stockout events: {patterns['total_stockout_events']}")
        print(f"   • Total lost sales opportunity: {patterns['total_lost_sales']:.2f} units")
        print(f"   • Average stockout duration: {patterns['avg_stockout_duration']:.1f} days")
        
        if patterns['worst_styles']:
            print(f"\n   Worst performing style:")
            worst = patterns['worst_styles'][0]
            print(f"   • Style: {worst['style']}")
            print(f"   • Lost sales: {worst['total_lost_sales']:.2f} units")
            print(f"   • Total stockout days: {worst['total_stockout_days']}")
        
        if patterns['worst_sites']:
            print(f"\n   Worst performing site:")
            worst = patterns['worst_sites'][0]
            print(f"   • Site: {worst['site']}")
            print(f"   • Lost sales: {worst['total_lost_sales']:.2f} units")
            print(f"   • Total stockout days: {worst['total_stockout_days']}")
        
        print()
        print("=" * 80)
        print("INSIGHTS & RECOMMENDATIONS")
        print("=" * 80)
        print()
        
        avg_lost_per_event = patterns['total_lost_sales'] / patterns['total_stockout_events']
        print(f"• Average lost sales per stockout event: {avg_lost_per_event:.2f} units")
        print(f"• This represents significant revenue opportunity loss")
        print(f"• Recommendation: Improve demand forecasting to prevent these stockouts")
        
        if patterns['avg_stockout_duration'] > 5:
            print(f"• Long stockout durations ({patterns['avg_stockout_duration']:.1f} days average)")
            print(f"• Recommendation: Implement faster replenishment processes")
        
        print()
        
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
