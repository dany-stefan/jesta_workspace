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

## Task 2: [Task Title]

dfsdfsds

### [Section headers to be filled based on task requirements]

---

## Task 3: [Task Title]
**Time Allocation:** [Time estimate]

### [Section headers to be filled based on task requirements]

---

## Summary & Recommendations
[Key takeaways and next steps]
