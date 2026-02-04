# Root Cause Analysis: Forecasting System Issues

## Executive Summary

This memo analyzes the critical issues affecting the current forecasting system and proposes a pragmatic roadmap for improvement. The system is experiencing high forecast error rates (~40% MAPE) and memory constraints that prevent scaling, resulting in significant lost sales due to stockouts and excess inventory costs.

## Problem Statement

The existing forecasting system suffers from three primary issues:

1. **High Forecast Error Rate**: ~40% MAPE (Mean Absolute Percentage Error)
2. **Memory Constraints**: System unable to scale to full product catalog
3. **Operational Impact**: Frequent stockouts and overstock situations

## Root Cause Analysis

### 1. High Forecast Error Rate (~40% MAPE)

#### Underlying Causes:
- **Insufficient Feature Engineering**: The model likely uses only basic time-series features without incorporating:
  - Promotional events and pricing changes
  - Seasonality patterns specific to fashion (e.g., seasonal collections, weather impact)
  - Product lifecycle stages (launch, growth, maturity, clearance)
  - Cross-product cannibalization effects
  
- **Inadequate Model Selection**: Single model approach may not capture diverse product behaviors:
  - Fast-fashion items have different patterns than classics
  - New launches vs. established products require different approaches
  - Store-specific local factors not accounted for

- **Data Quality Issues**: 
  - Missing or incorrect historical data
  - Inconsistent handling of promotional periods
  - Stockout periods treated as low demand rather than constrained supply

#### Evidence from Sample Data:
The `fashion_sample.csv` shows a clear stockout pattern (inventory reaching 0 on 2024-02-01 through 2024-02-10), but the system appears to have missed this demand signal. During restocking (2024-02-11), sales immediately resumed, indicating unmet demand.

### 2. Memory Constraints

#### Underlying Causes:
- **Inefficient Data Storage**: Likely storing full historical data in memory during training
- **Dense Model Architecture**: Possibly using deep learning models without optimization
- **Lack of Data Partitioning**: Not leveraging distributed computing or batch processing
- **Memory Leaks**: Potential issues with data pipeline not releasing resources

#### Technical Debt:
- System architecture not designed for horizontal scaling
- Monolithic approach rather than microservices
- No clear separation between training and inference pipelines

### 3. Operational Impact

#### Business Consequences:
- **Lost Sales**: Stockouts directly result in lost revenue and customer dissatisfaction
- **Excess Inventory Costs**: Over-forecasting leads to markdowns and carrying costs
- **Reduced Trust**: Stakeholders lose confidence in forecasting system
- **Manual Interventions**: Teams spend time manually adjusting forecasts

## Realistic Roadmap for Improvement

### Phase 1: Quick Wins (Weeks 1-4)

**Goal**: Reduce MAPE by 10-15% and improve system stability

#### Actions:
1. **Data Quality Improvements**
   - Implement stockout detection (see Part 2 implementation)
   - Flag constrained supply periods and exclude from training
   - Clean promotional data and ensure consistent labeling
   
2. **Feature Engineering**
   - Add day-of-week and holiday indicators
   - Calculate rolling averages (7, 14, 28 days)
   - Include price elasticity features (current_price / original_price)
   - Add product age (days since launch)

3. **Memory Optimization**
   - Switch to Polars for data processing (5-10x faster than pandas, lower memory)
   - Implement incremental learning approach
   - Use data streaming instead of loading all data

**Expected Outcome**: MAPE reduction to ~30-35%, system can handle 2x current product count

### Phase 2: Model Improvements (Weeks 5-12)

**Goal**: Further improve accuracy and add robustness

#### Actions:
1. **Ensemble Approach**
   - Implement lightweight models for different product segments:
     - New products (< 90 days): Simple moving averages with trend adjustment
     - Established products: LightGBM or similar gradient boosting
     - Seasonal products: Prophet or seasonal ARIMA
   
2. **Product Segmentation**
   - Cluster products by behavior (ABC analysis + velocity)
   - Apply specialized models per segment
   - Different forecast horizons for different segments

3. **Automated Retraining**
   - Weekly model updates with recent data
   - Performance monitoring and automatic model selection
   - A/B testing framework for model comparison

**Expected Outcome**: MAPE reduction to ~20-25%, improved forecast reliability

### Phase 3: Production Scale (Weeks 13-24)

**Goal**: Scale to full catalog and implement ML Ops best practices

#### Actions:
1. **Infrastructure Modernization**
   - Migrate to distributed computing (Dask or Spark)
   - Implement proper data versioning (DVC)
   - Set up model registry and experiment tracking (MLflow)
   
2. **Pipeline Automation**
   - CI/CD for model training and deployment
   - Automated data validation checks
   - Monitoring and alerting for model drift

3. **Advanced Features**
   - External data integration (weather, local events)
   - Cross-location transfer learning
   - Real-time forecast updates based on early sales signals

**Expected Outcome**: MAPE < 20%, system handles full catalog with room to scale

## Success Metrics

### Leading Indicators:
- MAPE reduction by phase (track weekly)
- System memory usage trending down
- Model training time reduction
- Data quality scores improving

### Lagging Indicators:
- Stockout frequency reduction
- Inventory turnover improvement
- Forecast bias (over/under forecasting) trending toward zero
- Reduced manual forecast adjustments

### Business Impact:
- Lost sales reduction ($ value)
- Inventory carrying cost reduction
- Customer satisfaction scores
- Forecast accuracy by product segment

## Risk Mitigation

### Technical Risks:
- **Risk**: New models perform worse than baseline
  - **Mitigation**: A/B testing, gradual rollout, easy rollback mechanism
  
- **Risk**: Memory issues persist despite optimizations
  - **Mitigation**: Phased product rollout, cloud scaling options

### Organizational Risks:
- **Risk**: Resistance to change from stakeholders
  - **Mitigation**: Regular communication, demonstrate quick wins, involve stakeholders in testing
  
- **Risk**: Data quality issues surface during implementation
  - **Mitigation**: Allocate time for data investigation, establish data governance

## Conclusion

The forecasting system issues are solvable through a combination of data quality improvements, smarter feature engineering, and modern ML infrastructure. The proposed three-phase approach balances quick wins with long-term sustainability, with realistic targets for MAPE reduction from ~40% to <20% over six months.

The key is to start with foundational fixes (data quality, basic features, memory optimization) before investing in complex models. This approach ensures each phase delivers measurable value while building toward a production-grade ML system.

## Appendix: Technical Choices Rationale

### Why Polars over Pandas?
- **Memory Efficiency**: 5-10x lower memory footprint
- **Speed**: Parallelized operations, lazy evaluation
- **Production Ready**: Rust-based, stable, and performant
- **Modern Design**: Better API for complex operations

### Why LightGBM?
- **Memory Efficient**: Histogram-based approach
- **Fast Training**: Faster than XGBoost on large datasets
- **Good Performance**: State-of-the-art accuracy with less complexity than deep learning
- **Interpretable**: Feature importance for stakeholder trust

### Why Segmentation?
- **One Size Doesn't Fit All**: Different products have fundamentally different demand patterns
- **Resource Efficiency**: Simple models for simple patterns, complex models only where needed
- **Maintainability**: Easier to debug and improve segment-specific models
- **Business Alignment**: Segments align with business categories (new/core/clearance)
