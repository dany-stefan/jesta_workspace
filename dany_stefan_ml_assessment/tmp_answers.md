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
