# Temporary Answers - Review & Edit Before Final Submission

## Task 1: Root Cause Memo (Concise One-Pager)

**1. Top 3 Reasons for 50% Error (Ranked by Impact)**

**(1) Forecasting Dead Stock / Wrong Product Mix (Primary Driver):**
The system forecasts 12.6M products, but most are dead stock or irrelevant combinations. In fashion retail, only active, in-stock, replenishable products should be forecasted. Forecasting everything wastes compute, causes OOM crashes, and inflates error metrics—making WMAPE look much worse than it is. Filtering to a realistic, active catalog is industry standard and would immediately cut error and stabilize the system.

**(2) Censored Demand from Stockouts:**
When inventory is zero, sales are always zero, but true demand may be much higher. The model treats these as "no demand" instead of "couldn’t serve demand," especially in high-velocity categories like Footwear. This leads to systematic underprediction for bestsellers and distorts learning. Made-to-Measure avoids this because it’s built-to-order, so all sales reflect true demand.

**(3) Missing Price/Markdown Features:**
Fashion demand is highly price-sensitive, especially during markdowns and clearance. If the model ignores price, it can’t distinguish between full-price and discounted demand, leading to persistent errors in categories with aggressive markdown cycles (e.g., Sportswear). Made-to-Measure is less affected due to stable pricing.


## Task 1, Question 2: Why does Footwear have 233% error while Made-to-Measure has 40%? What would you investigate? What hypotheses do you have?

The dramatic difference in error rates between Footwear (233%) and Made-to-Measure (40%) points to fundamental differences in product, sales, and demand patterns.

**Footwear:**
- High-velocity, high-SKU category with frequent stockouts, aggressive markdowns, and strong seasonality (e.g., back-to-school, holiday spikes).
- Inventory constraints are common: popular sizes/colors sell out quickly, leading to censored demand (zero sales during stockouts).
- Demand is highly sensitive to promotions, weather, and local events.
- Product churn is high: new models are launched frequently, and old ones are discontinued.
- The model likely treats zero sales as zero demand, missing the true demand signal during stockouts and markdowns.
- Errors are amplified by forecasting for dead stock and irrelevant SKUs.

**Made-to-Measure:**
- Low-velocity, low-SKU category with stable pricing and little to no inventory constraints.
- Sales are typically custom orders, so demand is less affected by stockouts or markdowns.
- Demand is more predictable, driven by appointments, events, or repeat customers.
- The model’s error is lower because the data is cleaner, less censored, and less affected by external factors.

**What would I investigate?**
- **Stockout frequency and duration:** Analyze inventory and sales data to quantify how often Footwear SKUs are out of stock versus Made-to-Measure.
- **SKU churn and catalog size:** Compare the number of active SKUs, discontinued products, and catalog turnover in both categories.
- **Promotion and markdown events:** Review historical pricing data to see how often Footwear is discounted and how demand responds.
- **Seasonality and event impact:** Overlay sales data with calendar events, weather, and local promotions to identify missed demand spikes.
- **Traffic and conversion data:** Use website analytics to compare traffic, conversion rates, and abandonment for Footwear vs. Made-to-Measure.
- **Customer behavior:** Investigate whether Footwear customers are more likely to switch products or sizes when their preferred option is unavailable.

**Hypotheses:**
1. Footwear error is inflated by frequent stockouts and dead stock, causing the model to miss true demand and over-forecast irrelevant SKUs.
2. Aggressive markdown cycles and seasonality in Footwear are not captured by the model, leading to missed demand surges.
3. Made-to-Measure benefits from stable pricing, low SKU churn, and predictable demand, resulting in lower error.
4. The model’s feature set is not tailored to category-specific patterns, causing systematic underperformance in Footwear.

**How to investigate:**
- Segment sales and inventory data by category, SKU, and store.
- Calculate the percentage of days each Footwear SKU is out of stock.
- Map price changes and markdown events to sales spikes.
- Use external data (e.g., Google Trends, weather, event calendars) to correlate with sales patterns.
- Analyze website traffic and conversion rates for both categories to identify demand signals not captured in sales data.

By investigating these areas, I can pinpoint the root causes of the error gap and recommend targeted fixes for each category.

**3. One Critical Week 1 Decision**

**Aggressively filter products before any model work.**
Only forecast active, in-stock, replenishable products with sales history. This immediately fixes OOM crashes, enables demos, and reveals true model performance. It’s a fast, high-impact data engineering win that unlocks all downstream improvements. Make the system stable first—then tackle censored demand and price features.

**Why this ordering matters for Week 1 prioritization:**
Dead stock filtering is a data engineering problem with immediate operational benefits (fixes OOM, enables demos). Stockout handling is an ML problem requiring domain expertise (censored demand modeling, survival analysis). Markdown features are a feature engineering problem requiring business logic. Attack in that sequence: make the system stable, then make it smart.

---



## Task 2: 90-Day Implementation Roadmap

### Did you identify the real problems or just symptoms?
This roadmap directly targets the root causes identified in Task 1: dead stock, censored demand, and missing price/seasonality features. Each task is designed to address these real problems, not just surface symptoms; for example, filtering dead stock fixes the denominator of error metrics, while stockout-aware modeling corrects misinformed demand signals.

### Is your roadmap realistic and well-prioritized?
The plan is sequenced for quick wins and sustainable progress: Week 1 delivers immediate stability and error reduction; subsequent weeks build on validated improvements. Risks are anticipated and mitigated at each step; effort estimates are based on typical engineering cycles for similar retail ML projects.

### Does your design address scale and maintainability?
All changes are staged, monitored, and rolled out with rollback options; dashboards and automated monitoring ensure the system remains robust as scale increases. Feature engineering and batch optimization are designed for maintainability, with continuous validation and feedback loops.

### Month 1 Goal: Reduce WMAPE to ≤35%
- **Week 1:** Filter out dead stock and wrong product mix; objective: only forecast active, replenishable SKUs; expected impact: immediate drop in WMAPE, resolve OOM crashes; effort: 3 days.
- **Week 2:** Implement stockout-aware demand modeling; objective: adjust for censored demand in high-velocity categories; expected impact: improved accuracy for Footwear/Sportswear; effort: 4 days.
- **Week 3-4:** Add price/markdown features to model; objective: capture price elasticity and promotional effects; expected impact: better forecasts during clearance events; effort: 1 week.

- **Key risk:** Data pipeline instability after aggressive filtering; **Mitigation:** Roll out changes in staging, monitor batch logs, and add rollback scripts.

### Month 2 Goal: WMAPE ≤30%; Demo-ready for clients
- **Week 1:** Engineer time-based features (seasonality, day-of-week, event flags); objective: improve model’s ability to capture demand cycles; expected impact: reduced error in Sportswear; effort: 1 week.
- **Week 2:** Retrain models with new features and validate on holdout sets; objective: ensure improvements generalize; expected impact: stable WMAPE; effort: 3 days.
- **Week 3-4:** Build dashboards for error tracking and business reporting; objective: communicate progress to stakeholders; expected impact: faster feedback loops; effort: 1 week.

- **Key risk:** Feature engineering does not yield expected gains; **Mitigation:** Run ablation tests and consult with domain experts for feature selection.

### Month 3 Goal: WMAPE ≤25%; Production stability
- **Week 1:** Optimize batch processing for memory and speed; objective: ensure weekly retraining is robust; expected impact: no OOM crashes, faster runs; effort: 4 days.
- **Week 2:** Set up automated model monitoring and alerting; objective: catch regressions early; expected impact: maintain accuracy over time; effort: 2 days.
- **Week 3-4:** Final client demo, collect feedback, and iterate; objective: ensure solution meets business needs; expected impact: client sign-off; effort: 1 week.

- **Key risk:** Model drift or unexpected data changes; **Mitigation:** Implement continuous monitoring and retraining triggers.

### Validation & Metrics
- Track WMAPE weekly by category and overall.
- Monitor OOM crash frequency and batch run times.
- Use dashboard to visualize error trends and feature impacts.
- Validate improvements with holdout sets and client feedback.

---

## Gantt Chart

See the visual Gantt chart in tmp_gantt.html for a story-driven, chart-based view of the 90-day roadmap.

---

## Task 3: Product Qualification Component Design

### Overview
The current system forecasts products that shouldn't be forecasted (e.g., items sitting 8 months with no sales, ecom getting all 150k products even though only 15k are online). The Product Qualification component is designed to intelligently filter and qualify products before forecasting, ensuring we only predict for active, replenishable items that truly need forecasts.

**See the complete visual system design diagrams:**
- **Detailed Architecture:** `product_qualification_diagram.html` - Complete pipeline with inputs, business rules, outputs, scale, and validation
- **Business Rules Flowchart:** `product_qualification_rules.html` - Category-specific decision tree

### 1. Inputs/Outputs

**Inputs:**
- **Sales History Data:** 3 years of daily transaction data (SKU, store, date, units_sold, revenue)
- **Inventory Data:** Current stock levels (SKU, store, on_hand_qty, replenishable_flag)
- **Product Metadata:** Category, subcategory, channel (physical/ecom), lifecycle stage (new/mature/discontinued)
- **Store/Ecom Flags:** Channel availability (is_online, is_in_store, store_list)
- **Restocking History:** Last restock date per SKU per location
- **Price/Markdown Data:** Current price, original price, clearance_flag, discount_percentage

**Data Format:** Polars DataFrame, processed in chunks to handle 150k SKUs × 61 stores = 9.15M rows

**Outputs:**
- **Qualified Product List:** DataFrame with (SKU, store, qualification_status, reason_code)
- **Qualification Metrics:** Count of products by status (active, dead_stock, new_product, seasonal_hold)
- **Forecast-Ready Dataset:** Filtered subset (3-4M products from 12.6M) with qualification metadata
- **Pipeline Integration:** Feeds directly into existing forecast model as pre-processing step

### 2. Business Rules

**Physical Stores Logic:**
- **Active Product Criteria:**
  - Sales in last 90 days > 0 OR
  - Restocked in last 60 days
  - Inventory > 0 AND replenishable = TRUE
  
- **Category Adjustments:**
  - Footwear: sales window = 60d (high velocity)
  - Sportswear: seasonal flag + 90d window
  - Made-to-measure: 180d window (low velocity)
  - Accessories: 120d window

**E-commerce Logic:**
- **Active Product Criteria:**
  - Currently listed online = TRUE
  - Sales in last 120 days > 0 OR
  - New product (launch < 30 days) AND inventory > 5
  - Not marked as "discontinued"

**New vs Mature Products:**
- **New Products (< 90 days since launch):**
  - Lower sales threshold (1+ sale)
  - Grace period: 30 days before qualification check
  - Higher inventory threshold (5+ units)
  
- **Mature Products (> 90 days):**
  - Standard sales thresholds apply
  - Stricter inventory rules
  - Replenishment pattern analysis

**High vs Low Volume Categories:**
- **High Volume (Footwear, Sportswear):**
  - Shorter lookback windows (60-90 days)
  - Focus on recent velocity
  - Stockout-aware qualification
  
- **Low Volume (Made-to-Measure, Luxury):**
  - Longer lookback windows (180+ days)
  - Consider pre-orders and custom orders
  - More lenient thresholds

**Dead Stock Criteria:**
- Zero sales for 180+ days
- No restocking in 120+ days
- Marked as discontinued
- Clearance phase > 90 days with no sales

### 3. Scale: Handling 150k SKUs × 61 stores without OOM

**Memory Optimization:**
- **Chunked Processing:** Process in batches of 500k rows using Polars lazy evaluation
- **Data Types:** Use categorical types for SKU/store, int16 for counts, float32 for metrics
- **Streaming:** Never load full 9.15M dataset into memory; process chunks and write incrementally

**Parallel Processing:**
- **Multi-threading:** Use Polars native parallelism (hit CPU, not memory)
- **Store-level Parallelization:** Process each store independently, then merge results
- **Category Batching:** Split by category (Footwear, Sportswear, etc.) for parallel execution

**Efficient Algorithms:**
- **Window Functions:** Use Polars rolling windows instead of manual loops
- **Hash Joins:** Pre-hash SKU/store combinations for fast lookups
- **Incremental Updates:** Only reprocess products with data changes, not entire catalog

**Storage Strategy:**
- **Intermediate Results:** Write qualification status to Parquet files (compressed, columnar)
- **Caching:** Cache product metadata and lookback thresholds (static data)
- **Garbage Collection:** Explicitly clear DataFrames after each chunk

**Scalability Limits:**
- Current: 150k SKUs × 61 stores = 9.15M rows (~2GB memory)
- Scaled: 500k SKUs × 200 stores = 100M rows (~20GB, still manageable with chunking)
- Future: Distributed processing with Dask/Ray if > 1B rows

### 4. Validation: How do you know it's working?

**Operational Metrics:**
- **Product Count Changes:** Track before/after qualification (expect 12.6M → 3-4M)
- **Memory Usage:** Monitor peak RAM during qualification (target < 4GB)
- **Processing Time:** Measure end-to-end runtime (target < 15 minutes for full catalog)
- **Error Rates:** Zero qualification logic errors (validated with unit tests)

**Business Metrics:**
- **Qualification Rate by Category:** % of products qualified per category (expect 20-30% overall)
- **False Negatives:** Products marked "dead" but then had sales (audit quarterly)
- **False Positives:** Products forecasted but never sold (audit monthly)
- **Forecast Coverage:** % of actual sales covered by qualified products (target > 95%)

**Model Impact Metrics:**
- **WMAPE Improvement:** Expect 15-25% reduction from filtering alone
- **OOM Crashes:** Track frequency (target: 0 crashes)
- **Training Speed:** Measure time savings from smaller dataset (expect 30-40% faster)
- **Forecast Accuracy by Category:** Compare before/after qualification

**Validation Workflow:**
1. **Weekly Audits:** Sample 100 random qualified products and verify sales activity
2. **Monthly Reports:** Dashboard showing qualification trends and error rates
3. **Quarterly Reviews:** Deep-dive with SMEs to adjust thresholds
4. **A/B Testing:** Run parallel forecasts with/without qualification for comparison

**Alert Triggers:**
- Qualification rate drops below 15% or exceeds 40%
- Processing time exceeds 30 minutes
- Memory usage exceeds 6GB
- False negative rate > 5%

**Success Criteria:**
- ✓ WMAPE reduced by at least 15% from qualification alone
- ✓ Zero OOM crashes for 4 consecutive weeks
- ✓ Processing time stable at < 15 minutes
- ✓ Stakeholder sign-off on qualification logic

---

**See complete visual diagrams:**
- System architecture: `product_qualification_diagram.html`
- Business rules flowchart: `product_qualification_rules.html`

---

## Product Qualification Component - Long Form Explanation

The Product Qualification component is designed to solve the critical issue of forecasting for products that should not be included in demand predictions—such as dead stock, discontinued items, or SKUs not available in the relevant channel. By acting as a robust pre-processing filter, this component ensures that only active, replenishable, and relevant products are passed to the forecasting model, dramatically improving accuracy and operational efficiency.

### 1. Inputs/Outputs

The system ingests several key data sources: sales history, inventory levels, product metadata, channel flags, restocking history, and price/markdown information. Sales history provides a multi-year record of transactions for each SKU and store, allowing the system to assess recent demand and identify patterns. Inventory data reveals which products are currently in stock and whether they can be replenished, while restocking history helps distinguish between genuinely dead stock and temporarily unavailable items. Product metadata and channel flags indicate whether a product is available online, in physical stores, or both, and whether it is new, mature, or discontinued. Price and markdown data are essential for understanding demand elasticity and promotional effects.

After applying qualification logic, the component outputs a filtered list of product-store combinations that meet the criteria for forecasting. Each qualified product is annotated with a status and reason code, providing transparency for downstream analysis. The output dataset is significantly reduced in size—typically from 12.6 million to 3–4 million rows—making it manageable for modeling and reporting. This qualified dataset replaces the raw product catalog as the input for all subsequent forecasting and analytics steps.

### 2. Business Rules

At the heart of the component is a business rules engine that applies tailored logic for different channels, product lifecycles, and category volumes. For physical stores, products must have recent sales (within the last 90 days) or have been restocked in the last 60 days, and must be in stock and marked as replenishable. Category-specific adjustments are made: high-velocity categories like Footwear use a shorter lookback window, while low-velocity categories like Made-to-Measure use a longer window. For e-commerce, products must be currently listed online, have recent sales (within 120 days), or be new launches with sufficient inventory. Discontinued products and those not actively listed online are excluded.

The rules also differentiate between new and mature products. New products (less than 90 days since launch) are given a grace period before qualification checks and require at least one sale and a higher inventory threshold to be included. Mature products are subject to stricter sales and inventory requirements, as well as replenishment pattern analysis. High-volume categories are evaluated with a focus on recent sales velocity and stockout-aware logic, while low-volume categories are assessed with more lenient thresholds and consideration for custom or pre-order items. Dead stock is systematically excluded based on extended periods of zero sales, lack of restocking, discontinued status, or prolonged clearance without sales.

### 3. Scale

To handle the immense scale of 150,000 SKUs across 61 stores—over 9 million product-store combinations—the component is engineered for memory efficiency and parallel processing. Data is processed in manageable chunks (typically 500,000 rows at a time) using Polars lazy evaluation, which prevents the system from loading the entire dataset into memory. Data types are optimized, with categorical encoding for SKUs and stores and compact numeric formats for counts and metrics. Polars’ native multi-threading enables parallel computation at both the store and category level, maximizing CPU utilization and minimizing runtime.

Efficient algorithms such as rolling window functions and hash joins are used for fast aggregation and lookups. Only products with data changes are reprocessed, reducing unnecessary computation. Intermediate results are written incrementally to compressed Parquet files, ensuring fast I/O and easy integration with downstream systems. The architecture is designed to scale up to 100 million rows with chunked processing, and can be extended to distributed frameworks like Dask or Ray for even larger datasets.

### 4. Validation

Validation is integral to the Product Qualification component, ensuring that the filtering logic is effective and that business goals are met. Operational metrics are tracked, including the reduction in product count, peak memory usage, processing time, and error rates. Business metrics such as qualification rate by category, false negatives (excluded products that later sell), false positives (included products that never sell), and forecast coverage are monitored to ensure the system is capturing true demand.

Model impact is measured by improvements in WMAPE, reduction in OOM crashes, faster training times, and enhanced forecast accuracy by category. Validation workflows include weekly audits of random qualified products, monthly reports on qualification trends and error rates, quarterly reviews with subject matter experts to refine thresholds, and A/B testing to compare forecasts with and without qualification. Alert triggers are set for abnormal qualification rates, excessive processing time or memory usage, and high false negative rates. Success is defined by a substantial reduction in WMAPE, elimination of OOM crashes, stable processing times, and stakeholder approval of the qualification logic.

By integrating these design principles, the Product Qualification component transforms the forecasting pipeline into a scalable, accurate, and business-aligned solution, ensuring that only the right products are forecasted and that resources are used efficiently.
