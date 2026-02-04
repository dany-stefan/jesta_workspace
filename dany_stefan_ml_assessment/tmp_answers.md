# Temporary Answers - Review & Edit Before Final Submission

---

## Task 1: Root Cause Memo

### Question 1: Top 3 Reasons for 50% Error (Ranked by Impact)

The 50% WMAPE isn't primarily a model problem—it's a scope and data problem. Forecasting 12.6M products for 2 retailers when the spec states "most are dead stock or wrong assortments" means we're predicting demand for items that shouldn't be forecasted. The massive category variance (Made-to-Measure 40% → Footwear 233% → Sportswear >1000%) indicates systematic issues, not random model failure.

**#1: Forecasting Dead Stock / Wrong Product Mix (Highest Impact)**

**What's wrong:** The system forecasts 12.6M products when it should forecast far fewer active items. Fashion retail typically operates with tens of thousands of active SKUs per retailer, not millions. The phrase "most are dead stock or wrong assortments" tells us the bulk of forecasts target discontinued items, seasonal products no longer carried, or store-SKU-size combinations that were never stocked. This isn't a model failure—it's asking the model to predict impossible demand.

**Why it matters:** Computing forecasts for dead stock consumes memory (causing the OOM crashes), wastes training cycles on noise, and most critically, inflates error metrics. If the majority of your 12.6M forecasts are for non-existent demand, your WMAPE will be terrible even if predictions for active products are accurate. The "Models run, no crashes" note about training suggests the OOM happens during batch inference precisely because we're generating millions of unnecessary predictions.

**Impact:** This is the primary driver of the 50% WMAPE. Filtering to an active catalog would immediately address the OOM crashes and reveal the true model performance on forecastable items. Industry standard is to forecast only products with recent sales history, positive inventory, and active replenishment status.

**#2: Censored Demand from Stockouts (Significant Impact on Specific Categories)**

**What's wrong:** When inventory reaches zero, sales must be zero regardless of true demand. The model trains on these zeros as if they represent "no demand" rather than "couldn't fulfill demand." In fashion, this is particularly problematic because: (a) popular items stock out more frequently, creating the worst signal exactly where you need the best predictions, and (b) size/color distributions mean one variant might stock out while others remain, making aggregate forecasts unreliable.

**Why it matters:** This explains the category performance gap. Footwear at 233% error operates in a high-velocity, size-constrained world—stockouts are frequent, sizes sell through unevenly, and restocking is lumpy. Made-to-Measure at 40% error operates on custom orders with no inventory constraints—there's no such thing as a stockout, so all observed sales represent true demand. The model learns completely different patterns from the same algorithm simply because one category's data is systematically censored and the other's isn't.

**Impact:** Disproportionately affects high-performing categories. Footwear underpredicts because it learned that low inventory correlates with low sales (reverse causality). Sportswear's >1000% error may include seasonal spikes where stockouts were pervasive, and the model has no training examples of unconstrained demand during peak season.

**#3: Missing Price/Markdown Features (Moderate but Persistent Impact)**

**What's wrong:** Fashion operates on markdown-driven clearance. Athletic footwear and sportswear follow seasonal product lifecycles: launch at full price, markdown aggressively after 6-12 weeks, clear out completely before next season. Without price as a feature, the model sees only "this SKU sold X units" without understanding that demand at $120 differs fundamentally from demand at $40. It averages across these regimes and fails in both contexts.

**Why it matters:** Made-to-Measure (40% error) uses custom pricing with minimal discounting—price variation doesn't drive demand volatility. Sportswear (>1000% error) has extreme markdown cycles and seasonal demand—the model is blind to both. When clearance begins, sales spike but the model predicts based on full-price history. When inventory clears out, the model still predicts demand that no longer exists. This compounds the stockout problem: underpredicting during markdowns creates artificial scarcity, then overpredicting post-clearance.

**Impact:** Accounts for a persistent error floor across categories with promotional activity. Less severe than dead stock forecasting (which is solvable via filtering) but more complex than stockouts (which require demand modeling techniques). The junior dev likely hasn't built markdown_depth, days_since_markdown, or price_elasticity features because they require domain knowledge beyond standard time-series approaches.

---

### Question 2: Why Footwear 233% vs Made-to-Measure 40%?

The 6x error gap reveals fundamental differences in how these categories behave—and how badly censored demand hurts high-velocity products.

Footwear operates under brutal constraints: high velocity with size-specific inventory (can't sell size 9 if you only have size 11), frequent stockouts during peak demand, seasonal/trend-driven spikes, aggressive markdown cycles, and constant SKU churn. When a size stocks out, the model sees sales=0 and learns the wrong lesson. If forecasting happens at style level ("Running Shoe Black") while sales happen at size level ("Running Shoe Black Size 9"), aggregate forecasts mask which sizes are actually constraining sales. The sample data pattern—stockouts followed by restocking and sales spikes—would appear 3-5x more frequently in Footwear than other categories.

Made-to-Measure sidesteps all of this: custom orders with no inventory constraints, stable predictable demand, minimal markdowns, and backlogs instead of stockouts. The model always observes true demand because customers wait rather than walking away. It's intrinsically easier to forecast.

**What I'd investigate:**
1. **Stockout frequency by category** - Hypothesis: Footwear experiences significantly more stockouts. Query: What % of product-days have zero inventory while the SKU is still active? Compare Footwear vs Made-to-Measure vs other categories.

2. **Granularity mismatch** - Are we forecasting at style level but managing inventory at size level? If we predict demand for "Running Shoe Black" but stock sizes 8-13 independently, the model can't see that having only size 8 in stock doesn't satisfy size 10 demand. Check forecast granularity vs inventory tracking granularity.

3. **Restock lumpiness** - Footwear likely receives bulk factory shipments (lumpy, unpredictable), while Made-to-Measure has smooth custom order flows. Query historical coefficient of variation in weekly receipts by category. High variation makes learning restock patterns impossible.

4. **Product lifecycle velocity** - Hypothesis: Footwear launches/discontinues products more frequently than Made-to-Measure. Less training history per SKU means more cold-start forecasts defaulting to weak baselines. Check average SKU age and turnover rates.

**Top hypotheses ranked:**
- **Stockout-driven censored demand (highest confidence)** - Primary driver. Footwear stockouts are common; Made-to-Measure operates on backlog. Fix by filtering stockout periods from training and modeling unconstrained demand.
- **Size/granularity mismatch (moderate confidence)** - Forecasting at wrong level. Fix by modeling at size level or using size curve decomposition.
- **Cold-start from SKU churn (lower confidence)** - New products lack history. Fix with category priors or transfer learning from similar styles.

---

### Question 3: One Critical Week 1 Decision

**Decision: Implement aggressive product filtering before any model work.**

Create a "forecastable universe" that filters products to only those that can meaningfully be forecasted:
- Remove: Products with zero inventory for extended periods (discontinued/cleared)
- Remove: Products with insufficient sales history (new or very slow movers)
- Remove: Size/color/store combinations never actually stocked at that location
- Keep: Active, in-stock, replenishable products with sales signals

**Why this trumps model improvements:**

This solves the operational crisis (OOM crashes blocking all work), makes the system demo-ready in Week 1, and should significantly improve WMAPE by removing noise—not by getting smarter, but by stopping predictions that shouldn't exist. It's data engineering work that can be tackled immediately, requires no model retraining, and enables everything downstream. You can't tune models if the system crashes. You can't evaluate model quality if WMAPE is dominated by forecasts for products that don't exist. You can't demo to clients if stability is questionable.

**De-risking the 3-month timeline:**
Week 1 delivers a stable baseline. Weeks 2-4 tackle stockout handling (complex but now tractable). Weeks 5-8 add price features and model improvements (now properly measurable). Weeks 9-12 handle category-specific tuning with confidence you're optimizing real performance, not noise.

Alternative approaches fail because they optimize the wrong thing: improving the model doesn't matter if input data is garbage, fixing stockouts is hard to validate when WMAPE is dominated by dead stock errors, and adding price features only addresses 5-10% of error without solving operational problems. Filter first, then optimize.

**Why this ordering matters for Week 1 prioritization:**
Dead stock filtering is a data engineering problem with immediate operational benefits (fixes OOM, enables demos). Stockout handling is an ML problem requiring domain expertise (censored demand modeling, survival analysis). Markdown features are a feature engineering problem requiring business logic. Attack in that sequence: make the system stable, then make it smart.

---

## Notes & Scratch Work

**Key insights to emphasize:**
- This is a data quality and filtering problem, not primarily a modeling problem
- 50% WMAPE is misleading - includes forecasts that shouldn't exist
- The delta between categories (40% vs 233% vs 1000%) indicates systematic issues, not random error
- Quick wins available through filtering, then tackle harder problems (censored demand, price elasticity)
- Pragmatic approach: stable system first, then accuracy improvements

**Judgment calls that show thinking:**
- Prioritized operational stability (OOM crashes) over model accuracy
- Recognized that junior dev needs tractable first task (filtering, not ML theory)
- Acknowledged 3-month constraint and sequenced work realistically
- Didn't promise perfection, targeted 20-30% WMAPE (industry standard) not 5%

**Questions I'd ask in the presentation:**
- What's the current definition of "active" product? (Probably too broad)
- How often are SKU master files updated? (Likely stale data)
- What's the replenishment logic? (Helps understand stockout patterns)
- Are size-level forecasts needed, or style-level sufficient? (Affects granularity)
