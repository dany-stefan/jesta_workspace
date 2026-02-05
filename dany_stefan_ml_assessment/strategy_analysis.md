# Strategic Analysis & Architecture

## Part 1: Strategy & Architecture (40%)

---

## Task 1: Root Cause Memo

### Q1:
The problem I am understanding here is not one of implementation because the model runs and produces forecasts. It is also not a lack of backtesting data, as it spans 3 years of daily data points, and the forecast runs millions of data points. Quantity here is not the issue. It appears that the quality of the data is the problem. Indeed, most of the data points can be dead stock or the wrong assortment of products that are being forecasted. We are most probably forecasting inactive products that actually have no demand anymore, or products that are not being sold anymore in the stores, either due to inventory at 0, no restocking, or no more sales. This creates a lot of noise in the data and makes the model look worse than it actually is. We must focus on forecasting the right products that are active and replenishable. This is a data engineering problem that needs to be solved first before any modeling improvements can be made.


The largest reason for 50% error is indeed the dead stock for products that should not be forecasted at all. To address dead stock, it is wrong to be forecasting for products that won't see the light of day, as they are not being sold anymore or the stock is zero. Suppose we remove the bloated data and trim it to a subset that is relevant to forecast; then we avoid noise in the training data, predict for truly active products, and reduce memory usage. This alone can improve the WMAPE and cut that number in half, as it is the largest cause for the error. The impact will give more relevant predictions and reduce memory usage, thus avoiding OOM crashes and enabling more efficient batch processing. Your chunk sizes will be smaller to process and then train. Moreover, training time will be reduced as well. We want our subset to include products that are truly active and replenishable. This matters to produce relevant predictions and with relevant input. We should limit inflating our predictions. Industry standard is filtering for an active catalog. The nuance here is to include in this subset replenishable products that have a history of sales and are in stock or can be restocked. Limited stock products or discontinued items can't be included in the training set; this is the wrong product mix problem. There should be a filtering that marks active or inactive products based on sales history, inventory levels, and replenishment patterns. We can't treat products that are sitting on the shelves as products that have demand; thus, we must filter them out. Also, ones that don't replenish can't be forecasted, as they will never be sold again.

The second reason is the misinformed demand that is the victim of cause and effect. Zero stock causes zero sales, but zero sales does not mean zero demand. The model is being misinformed that there is no demand, when in reality there is demand that is not being served due to stockouts. This is especially true for high-velocity categories like Footwear. It is even worse for Sportswear, where seasonality is crucial based on the location of the store and the weather customers live through the year. Perhaps the largest error in the Sportswear category is due to the lack of seasonality, treating that category wrongfully compared to others that don't depend so much on it. The model treats these as no demand instead of could-not-serve demand. This leads to systematic underprediction for bestsellers and distorts learning. This not only reduces forecast accuracy for bestsellers but also leads to lost sales opportunities and poor inventory planning. This has cascading effects to miss peak demand cycles, under-allocate inventory, and ultimately lost revenue.


The last reason for the error can be missing price features. I can think of the luxury space where people eye a product but only purchase once they see a discount. Fashion is price-sensitive, and the model must have features to know when sales happen because of a clearance event, sale, or cycle in the year with holidays, for example, where that happens. Demand varies between these factors, and the model must be made aware of them to not underfit its predictions. This means it cannot learn the true relationship between price changes and demand spikes, especially during clearance or promotional events. As a result, the model will systematically miss demand surges tied to markdowns.

### Q2:
The difference comes from these categories having fundamentally different product, sales, and demand patterns. Already, footwear addresses one body part, whereas made-to-measure can dress your whole body with products. Even given recent hype trends around footwear, human psychology affects this category more than made-to-measure. It is less mainstream. This affects the modeling of these categories.

Footwear is high-velocity with many SKUs, frequent stockouts, aggressive markdowns, and strong seasonality. Inventory takes a hit with some variations (e.g., color) more popular than others; thus, censored demand problems arise where out-of-stock doesn't mean low demand.

Made-to-measure is low-velocity, where the inventory pipeline is more controlled and prices stay fixed, as it caters to a niche audience too, with custom orders. Thus, demand is more predictable and less affected by stockouts or markdowns. The model's error is lower because the data is cleaner, less censored, and less affected by external factors. Less error can come from the nature of the category.

I will investigate stockout frequency, SKU churn on active products or less popular products, markdown events and their frequency. Seasonality is another one, and traffic on websites measuring abandonment rates.

My hypotheses are that footwear error is inflated by frequent stockouts and dead stock, causing the model to miss true demand and over-forecast irrelevant SKUs. Aggressive markdown cycles and seasonality in footwear are not captured by the model, leading to missed demand surges. Made-to-measure benefits from stable pricing, low SKU churn, and predictable demand, resulting in lower error.

The model's feature set is not tailored to category-specific patterns, causing systematic underperformance in footwear.

### Q3:
A quick win I would do is set up a window of replenishable time—if the product saw a restock in the last x days, then we can mark it as an active catalog product. This eliminates what happens in the back-end inventory supply pipeline. We focus on what we can work with and the current facts. This means our subset has active, in-stock, replenishable products with sales history. This immediately fixes OOM crashes, enables demos, and reveals model performance improvements.


For business folks, I can show them progress. Even tackling the memory issue first and showing a quick result time is enough to show progress. This unlocks downstream wait times and holdups. Dead stock is the quickest win, with a window variable we can set and tune later. Make the system stable first—then tackle censored demand and price features. Must think agile, modular, and iterative. I can fix things in my domain first, which is data engineering and computer processing. If I can speed things up, I do it first. Then, feature engineering and model improvements can come later, where I must collaborate with domain experts.

---

## Task 2: 90-Day Plan
Assumptions:
- Junior has senior support for architecture and code reviews.
- Access to necessary data and computing resources is available.
- Already onboarded with Pandas and half onboarded with Polars (senior will provide resources to onboard him quickly).
- Tracking is agile in Jira tickets with weekly check-ins.
- Quick wins are prioritized to show progress.
- Alarms are sounded early for any blockers.


**Month 1 Goal:** [WMAPE target = reduce further by up to 1/2 -> new target number: (WMAPE <= 50-25%)]  
**GOAL:** Reduce batch size, reduce OOM crashes, error reduction, and demonstrate initial WMAPE improvement.  
**IMPACT:** HIGH IMPACT, LOW EFFORT  
**RISK SPILLING OVER:** LOW  
**NORTH STAR:** Finish early to start Month 2 early. (Senior to ensure all tools at disposal.)  

**Week #:** [Task] → Expected impact: [metric] [effort]  
**Week 1:** [Filter out inactive or non-replenishable products, inventory=0, known rule-set] → Expected impact: Reduce batch load size. [Batch size in MB reduced by 25% for training set.] [15h to analyse drops in inventory, speak to SMEs about non-replenishable products + 10h to implement filtering logic + 5h to test and validate + 5h buffer + 5h ramp-up on tools = 40h]  
**Week 2:** [Filter dead stock, sales=0, research a window of X time for zero sales period, mark no longer active purge] → Expected impact: Reduce batch load size and training time. [Batch size in MB reduced by 25%, faster training in ms compare with benchmark.] [20h research the best window period with SME and experiment with small set + 10h implement filtering logic and combinations + 5h test training speed + 5h buffer = 40h]  
**Checkpoint:** Validate reduced memory usage and training time without OOM crashes. (Dataset reduced from 12.6M to ~3-4M products.)  
**Week 3:** [Explore threads and parallel processing of the batch load in Python, no cloud ETL services, make it elegant and reproducible and scalable for other clients and more data points] → Expected impact: Even faster data processing in parallel by splitting in chunks, ready for training. [The ETL load should go at least twice as fast, reduce deadlocking and hanging, hit the CPU not the memory.] [15h research best practices for parallel processing in Polars + 20h implement and test for re-stitching correctly the chunks or keep separate for downstream + 5h buffer = 40h]  
**Week 4:** [Make last week's code modular and reusable components, no API blackbox or agentic orchestration, setup monitoring tools for training speed will use in the future, have time to start Month 2 tasks] → Expected impact: Futureproof, think high-level, train the junior what it means to document and leave your code to the next guy. [Learn a new design pattern almost creating in-house SDK, object-oriented or polymorphism - learn something new.] [20h refactor code to be modular + 3h document and create examples + 17h buffer = 40h]  

**Key risk:** [What could go wrong] → Mitigation: [How you'd handle it]  
- Junior gets stuck on Polars and parallel processing → Mitigation: Senior to provide resources and do pair programming sessions early in week 2 (deadlocks happening with threads, hanging time). [LIKELY TO HAPPEN, important to unblock fast]
- Get lost in week 4 with refactoring and over-engineering → Mitigation: Senior to review progress mid-week and ensure scope is controlled, no scope bleed. [LESS LIKELY, easy to catch, skip and move on if happens]
- Data can corrupt itself when splitting in chunks → Mitigation: Add unit tests and data validation after each processing step to ensure integrity. [POSSIBLE, but easy to catch with tests, number of rows should match after re-stitching]
- Filtering may remove too many products → Mitigation: Validate filtering logic with SMEs and run A/B tests (X window period) on a small subset before full rollout. [POSSIBLE and CRUCIAL]


**Month 2 Goal:** [WMAPE target = reduce further by up to 1/4 -> new target number: (WMAPE <= 37-18%)]  
**GOAL:** Feature engineer, address censored demand, and adjust price sensitivity.  
**IMPACT:** HIGH IMPACT, HIGH EFFORT  
**RISK SPILLING OVER:** HIGH  
**NORTH STAR:** Don't over-engineer. Stick to set of features. Address roadblocks quickly to not spill over. (Senior to prompt for roadblocks early because we tend to smile and not say anything.)  

**Week #:** [Task] → Expected impact: [metric] [effort]  
**Week 1:** [Start with simple features, one-hot encode (0 or 1) categorical features to numerical regression, do regression based engineering, describe each feature column with stats, locate outlier based on 95th s.d., have flags for discounts, events, holidays and day of the week, fill missing values with median/mean, combine interaction features (category and season), lag features, normalize feature to range denominator (shoe size based on inventory orders or not), I'd explore intra-category features, maybe group categories together like homegoods and sportswear that are cheap for the masses categories and explore more than just product level but go a higher level of abstraction up] → Expected impact: Standardize dataset ready for numerical regression forecasting. [Normal distribution on feature columns, N/A values, s.d. amount.] [10h exploring how the data looks like + 25h implement feature engineering logic + 2h debrief with senior about how the data looks and findings (note on data collection improvements, more or less columns, skips material choices, color choice) + 5h buffer = 40h]  
**Week 2:** [Stockout feature engineering (duration, lags (moving average sales or no stock duration), flags)] → Expected impact: Tackles censored demand problem (ongoing demand, 0 stock, recognize lack of inventory not lack of demand), directly impact WMAPE, sub-problem of classification stockout OR NOT. [Lagged indicators, can they cause demand to drop, correlation matrix or tree based feature importance, how can we affect the demand prediction based on stock we can control.] [20h to implement new stockout features + 20h to test sub-problem classification model to predict stockout OR NOT, feature importance analysis = 40h]  
**Week 3:** [Price elasticity feature engineering: discount flag, discount causation, percentage, price x promotion, price x season, price relative to category (hot accessory item)] → Expected impact: Contain highly volatile price changes and discounts combined with their cause (holidays). [Lower MAE in periods of discounts, have holding datasets to test smaller sets include/exclude features or pairings, overfit too much.] [10h feature implementation in the dataset + 25h test on holdout sets to validate impact + 5h buffer = 40h]  
**Checkpoint:** Validate feature impact on WMAPE using holdout sets see which are most important. (Aim for at least 5% WMAPE reduction from Month 1.)  
**Week 4:** [Set up monitoring for different accuracy measures: precision/recall for classification stockout feature, report based analysis on correlation matrix or feature importance] → Expected impact: Have visibility to see what is pertinent to include or exclude as a feature, be able to synthesize for leadership what is impactful by how much WMAPE we save. [MAE, WMAPE, correlation, time to train.] [15h gather all metrics needed to monitor variants + 20h run the predictions and results + 5h debugging = 40h]  

**Key risk:** [What could go wrong] → Mitigation: [How you'd handle it]  
- Wrong logic for feature calculations (lag) → Mitigation: Senior to review doing backward engineering see the most relevant feature (focus on most important first) and work backwards to the math logic. [LIKELY TO HAPPEN, important to catch early]
- Overfitting with too many features → Mitigation: Holdout sets, remove low importance features, early stopping to halt training when overfitting happens (catch it early) (because clients can span from sportswear that is high volatile and for the masses to luxury niche markets the model should be able to cover both ranges holistically without over compensating for one). [POSSIBLE and CRUCIAL]
- Stakeholder misalignment on key metrics → Mitigation: Early alignment meetings to set expectations and agree on success criteria. [LESS LIKELY, easy to catch with meetings]
- Scope creep with too many features and losing track of 3-month MVP timeline → Mitigation: Senior to keep junior on track with weekly check-ins and prioritization. [POSSIBLE, but easy to catch with weekly check-ins]
- Lack of documentation and knowledge transfer → Mitigation: Junior to document feature engineering steps and rationale for future reference. [LESS LIKELY, easy to catch with reviews]


**Month 3 Goal:** [WMAPE target = reduce further by up to 1/4 -> new target number: (WMAPE <= 28-13%)]  
**GOAL:** Finalize feature enhancements, optimize model parameters (grid search) and compute (parallelism), monitoring and production readiness (CI/CD).  
**IMPACT:** LOW IMPACT, MEDIUM EFFORT  
**RISK SPILLING OVER:** MEDIUM (last-minute issues, procrastination from Month 2)  
**NORTH STAR:** Stabilize and think of edge cases. Cover all bases to limit omissions. (Senior to play devil's advocate here.)  

**Week #:** [Task] → Expected impact: [metric] [effort]  
**Week 1:** [Leave time for refinement from last month, choose the very best features with grid search, have the train/test split and test with many simulated clients, buffer for last month's overflow] → Expected impact: Drive value to results for reducing the accuracy further, deliver and KT to best features, finalize analysis done on sub-features to be able to reuse in the future. [Evaluate difference between train and test MAE values, see overfit gap, see the tree-based models feature importance metric (XGBoost, Random Forest, LGBM), must see 10% reduction in MAE and at least 5% improvement on the WMAPE.] [25h refine the final list of features + 10h run grid search experiments + 5h buffer = 40h]  
**Week 2:** [Run end-to-end to see processing and training and testing speed and debug errors] → Expected impact: Polish data type errors, identify where it takes too long to process. [Seconds timestamp, logging, verify no memory crashes occur, if feature selection takes too much memory = trim down.] [30h run and rerun + 5h debug (always unexpected caching bugs) + 5h buffer = 40h]  
**Week 3:** [Integrate logging in an alerts and monitoring platform, release the model using CI/CD and model VCS] → Expected impact: Readiness for production and reusable for other clients. [See how well the model maintains accuracy, systems integration tests.] [15h monitoring platform + 20h CI/CD pipeline + 5h buffer = 40h]  
**Week 4:** [Prep a MVP BETA of the model and dataset to present] → Expected impact: Show that the model can be deployed and integrated in the client's infrastructure. [Uptime, CPU compute, build time, dependencies can download.] [25h integration and prep + 10h dry run + 5h buffer = 40h]  
**Checkpoint:** Deployable model that is trained and tested ready to integrate for the client's stack. (Aim for at least 5% WMAPE reduction from Month 2.)

**Key risk:** [What could go wrong] → Mitigation: [How you'd handle it]  
- Integration with CI/CD and client's infrastructure (lack of requirements from client) → Mitigation: Early meetings to gather requirements and align on expectations. [POSSIBLE, but easy to catch with early meetings]
- Last-minute bugs and issues → Mitigation: Buffer time.
- Performance bottle necks → Mitigation: Profiling techniques, feature selection based on profile or released model.
- Security concerns when integrating with client's systems → Mitigation: Follow best practices and consult with security experts (use authentication, protect with API keys).  


== 3-month timeline => WMAPE reduced from 50% to [target ~ 20% +/- 5%]  
** See gantt chart picture **

---

## Task 3: System Desin
hjgjhffhj

### [Section headers to be filled based on task requirements]

---

## Summary & Recommendations
[Key takeaways and next steps]
