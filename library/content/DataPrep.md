#  Data preparation is an importance influencer in model accuracy and outcome

If you are a developer or line of business person reading this, you are our target audience!  However, a small amount of "Data Thinking" or Data Science is required.  Machine learning models are only as good as the data put into them.  For this reason, we have a whole section dedicated to Data Prep and the reasoning behind that.  Common things to watch out for are missing timestamps or missing "item IDs", having 0's when in fact those values are missing, uniqueness of sales by item by timestamp (aggregation level), and extreme values.  "Dirty data" can affect the accuracy of Forecast models.

In terms of data, Forecasting works best on "dense" data. When, per timestamp and "item" to forecast, there is almost always a data point.  Examples of dense data include high-volume transactional consumer demand, call center demand, IT infrastructure demand, location-based service needs, electricity use.  "Sparse" data is when per timestamp and item very few sales happen.  Examples of sparse data are when the SKU is so targeted that it does not sell frequently, sales order data, or financial revenue numbers that are summarized per month.  Sparse data is difficult to forecast because as a time series there is not enough of it to establish a pattern.  Time series patterns are used to predict when and with what amplitude a particular "item target value" will occur in the future.  

For additional best practices and recommendations on data preparation, focused on sales and demand planning, but also generally applicable, refer to the [Amazon Forecast Data Set Guidance for Sales and Demand Planning](../../ForecastDatasetGuidanceSales.md).


**Developers:**  [Use AWS Glue DataBrew](https://aws.amazon.com/glue/features/databrew/), a data preparation UI tool, to clean data and save TTS to S3.  TODO link 5min video<br />

**Data Scientists:** We have DataPrep Jupyter notebook templates.  We have included common data prep steps we have noticed in customers' data.  

- If data is Hourly or below - [use the regular DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb)
- If data is Daily or Weekly - [use the weekly DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi_weekly.ipynb) <br />


## Best practices

Following are Best Practices for developing the most accurate Amazon Forecast models (or Predictors).  
1) **Make sure you know how success is measured**, i.e. metrics that matter for the business problem.  **Amazon Forecast automatically calculates for you the wQL, WAPE, and RMSE from the Predictor backtests.**  For probabilistic forecasts, we think wQL is the best error measure.

- Custom metrics can be calculated from Predictor backtest exports and from the Forecast export using hold-out data.

- Improving forecast accuracy for specific items—such as those with higher prices or higher costs—is often more important than optimizing for all items.  By exporting the Predictor backtest exports, item-level accuracy can be calculate for specific items or groups of items, without needing a hold-out data set.  
- For retailers specifically, not all SKUs are treated equally. Usually 80% of revenue is driven by 20% of SKUs, and retailers look to optimize forecasting accuracy for those top 20% SKUs.  Evaluating how the model, which is trained on all the SKUs, performs against those top 20% SKUs provides more meaningful insights on how a better forecasting model can have a direct impact on business objectives.
- Alternatively, you may look instead to optimize your forecasting models for specific departments. For example, for an electronic manufacturer, the departments selling the primary products may be more important than the departments selling accessory products, encouraging the manufacturer to optimize accuracy for the primary departments. 

2) **Pre-segmentation of data, call this your sample data.** For example, most data follows approx 80/20 rule, where 20% of the items are top-selling; the rest 80% of items are low-volume, long-tail.  Not all items have business value to merit the effort of forecasting.  **A good first sample is the 20% dense time series sample.** 

- One beginner mistake to avoid, is the thinking that small data is "better for testing".  Amazon Forecast processing steps are built for large data, they do not linearly scale with data size.  So, a very small sample of data will take just as long to run as a large sample.  Also, a small sample of data will very likely get poor results.

- Think of a neural network that trains best with many different weights as inputs.  If you decide to "test" with only 1-10 time series, this will often cause poor results, since there won't be enough inputs to train a global model.  Instead, Amazon Forecast will be forced to use Traditional Statistical local models.   
- When it comes to sparse datasets, you will need to do some experimentation. Some ideas:
  - Try NPTS algorithm in Amazon Forecast, which works better for intermittent demand patterns, or 
  - Aggregate your data at a higher frequency (Weekly instead of Daily)
  - Group sparse items at a higher product-group level.
  - Often the sparse items benefit from being trained in a Deep Learning global model.  That global model may have lousy accuracy, but the the sparse items in the model could have higher accuracy than if they were trained by themselves.

3) **Decisions:**

​	3.1) **What is your forecast time unit granularity?** For example, if you want to predict with 
​	weekly granularity, answer = “W”.

​			Choices are: Y|M|W|D|H|30min|15min|10min|5min|1min

​	3.2) **How many time units do you want to forecast? Call this forecast length.** For example, if your time unit is Hour, then if you want to forecast out 1 week, that would be 24*7 = 168 hours, so forecast length = 168.

​			Rule: Forecast length cannot be longer than 1/4 of training data 

​	3.3) **What is the time granularity for your data?**. For example, if your time unit is Hour, answer = "H".  

​			Choices are: Y|M|W|D|H|30min|15min|10min|5min|1min

​			Rule: Data granularity can be <= forecast granularity.

> Note:  Forecast can import data that isn't aligned with the collection frequency specified in the [CreateDataset](https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html) operation. For example, you can import data for which the collection frequency is hourly and some of the data isn't timestamped at the top of the hour (02:20, 02:45). Forecast aggregates the data to match the aligned value. 

4) **Identify columns in your data that you will map to: timestamp, item_id, target_value**.  The item_id should identify unique time series.  Typically item_id is a product ID.  Target_value is often a sales quantity.  The combination of timestamp, item_id, target_value should describe the historical sales for a particular product. [See documentation for more details.](https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html)

5) **Check for uniqueness.**  Each column in your Forecast dataset represents either a forecast *dimension* or *feature*. Forecast dimensions uniquely identify things you want to forecast, such item, store, or location. Features include any parameters in your data that vary across time (except the timestamp which is a dimension), such as 'sales_quantity'.

When you groupby timestamp and forecast dimensions, you should see only 1 'sales_quantity'. If you see more than 1, maybe you have another dimension such as sales location?  

Adjust your definition of "timestamp" and "item_id" such that at your chosen aggregation level, per time series, per timestamp, the count of unique "target_value" should only be 1. 

6) **Possibly, but not required right away, identify other data you think in future might help inform forecasts** – example Prices, Promotions, Stock-out dates, Holidays.

7) **Check your timestamp format**.  Should be dates only for daily or higher data time frequency (value in Step 3.3) .  The timestamp should have HH:mm:ss if data time frequency is hourly or lower.

​		 “yyyy-MM-dd” if DataFrequency is Daily or higher

8) **Pay special attention to gaps or 0’s in your data. Pro tip: convert all 0’s to nulls,** then let Amazon Forecast do automatic null-filling through its Featurization settings.  See [the null-filling syntax](https://docs.aws.amazon.com/forecast/latest/dg/howitworks-missing-values.html).

- If you're forecasting product demand for a retail store and an item is sold out or unavailable, there would be no sales data to record while that item is out of stock. We recommend that you fill the gaps in the historic sales data or target time series with NaN instead of 0. Filling with 0, the model might learn wrongly to bias forecasts toward 0. 
- **Differentiate between out of stock and end of life**.  You may want to either fill missing values differently or have separate related time series for end of life products/dates and stock-outs by products/dates. 

**Note: special consideration for cold-start or new product introductions**.<a name="coldstart"/>  For best results, do not include new items in your training data.  Do include new items in the inference data.  If fewer than 5 data points exist per new item, be sure to fill missing values explicitly for the new items with "NaN"; otherwise the cold-start items will be silently dropped.  For training, keep the [default null-filling frontfill= "none"](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#null-filling).

**Above new items advice assumes new items are the exception** and you have a majority set of "core" items with long histories.  For some customers, their items are almost all short-lived, so at any point in time, items are mostly either new or near end-of-life.  In this case, try to see if you have a higher-level item group that represents "substitution items" grouping.  Can you build a model at this substitution item_grouping level?  Otherwise, the only other option is to try the Deep Learning algorithms with metadata that ties together items, which may be in various phases of their life cycles, and are all included in the training data.


 
<br><br>
[Return to Table of Contents](../README.md)
