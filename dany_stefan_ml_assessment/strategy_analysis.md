# Strategic Analysis & Architecture

## Part 1: Strategy & Architecture (40%)

---

## Task 1: Root Cause Memo

### Problem Understanding
The problem I am understanding here is not one of implementation because the model runs and produces forecasts. It is also not a lack of backtesting data as it spans 3 years of daily datapoints and the forcast runs millions of datapoints. Quantity here is not the issue. It appears that the quality of the data is the problem. Indeed, most of the datapoints can be dead stock or wrong assortment of products that are being forecasted. We are most probably fprcasting inactive products that have no demand anymore or products that are not being sold anymore in the stores. This creates a lot of noise in the data and makes the model look worse than it actually is.

The largest reason for 50% error is indeed the dead stock/wrong product mix for products that should not be forecasted at all. To address dead stock.  It is wrong to be forcasting for products that won't see the light of day as they are not being sold anymore. This creates a lot of noise in the data and makes the model look worse than it actually is. Suppose we remove the bloated data and trim it to a subset that is relevant to forcast, then we avoid noise in the training data, predict for trully active products and reduce memory usage. This alone can improve the WMAPE from 50% and cut that number in half as it is the largest cause for the error. The impact will give more relevant predictions and reduce memory usage, thus, avoiding OOM crashes and more efficient batch processing. Your chunck sizes will be samller to process and then train. Moreover, training time will be reduced as well. We want our subset to include products that are truly active and replenishable. This matters to produce relevant predictions and with relevant input.

### Root Causes Identified
[List and explain the real problems, not just symptoms]

### Supporting Evidence
[Charts, data, and analysis supporting your diagnosis]

### Impact Assessment
[Quantify the impact of each root cause]

---

## Task 2: [Task Title]
**Time Allocation:** [Time estimate]

### [Section headers to be filled based on task requirements]

---

## Task 3: [Task Title]
**Time Allocation:** [Time estimate]

### [Section headers to be filled based on task requirements]

---

## Summary & Recommendations
[Key takeaways and next steps]
