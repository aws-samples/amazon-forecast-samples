# Amazon Forecast Introduction, Best Practices, and Cheat Sheet Tutorial

##### Table of Contents  
* [Amazon Forecast Introduction](#intro)  
  * [Mapping your data into time series](#mapping)
  * [Data Prep Best Practices](#dataprep)
* [Getting Started with Amazon Forecast Best Practices](#bestpractice)  
* [Getting Started Tutorial](#tutorial)
* [Iterating Models What-if Best Practices](#iteratebp)
* [Generating Forecasts](#forecastinference)
* [Example Notebooks](#notebooks)
* [Demos/Workshops](#workshops)
* [More Resources](#moreresources)



![](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/forecast_overview.png)

<a name="intro"/>


## Amazon Forecast Introduction

Amazon Forecast is a fully-managed AWS service, using the same deep learning probabilistic forecast technology developed at Amazon (which offers over 400million different products and ships Billions of packages in 185 different countries every day).  Amazon Forecast addresses the challenge of more accurate forecasting.  Users do not need to be machine learning experts in order to achieve accuracy levels that used to take months of engineering. <br>
<br>
For more information, [see our documentation](https://docs.aws.amazon.com/forecast/latest/dg/getting-started.html).

Amazon Forecast's strength is its deep learning algorithms.  Traditional statistical methods, sometimes called "local models", are able to learn one time series at a time.  That means if you have 20K items to forecast, then 20K traditional models are required; each model unable to learn from other models.  Traditional statistical algorithms include:  Exponential Smoothing (ETS), ARIMA, NPTS, and Prophet.  These traditional algorithms are included in Amazon Forecast.

Deep learning algorithms, sometimes called "global models", are able to learn using more than 1 time series at a time.  That means if you have 20K items to forecast, and they have interrelationships between them such as item-affinity or cannibalization, such behaviors can be learned by inputting them all into a single model.  Amazon Forecast's proprietary deep learning algorithms include:  DeepAR+ (an LSTM version of RNN) and CNN-QR (a quantile regression version of CNN, a neural network topology typically used in computer vision). 

### Is Amazon Forecast a Good Fit?

Not all machine learning problems are forecasting problems.  The first question to ask is "Does my business problem include time series in its statement?"  For example, do you need a particular value only at a particular time and date in the future?  Forecasting is not a good fit for general, static (where the particular date/time does not matter) problems, such as fraud detection or recommended movie titles to users.  There are much quicker solutions to static problems.  

In addition to having time series data, the data itself should be "dense" and with long histories.

This is summarized in the following table:<a name="datasize"/>

| Criteria                                                     | Amazon Forecast Algorithm class                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Large dataset with up to 5 million time series with similar underlying patterns + seasonal effects + related data. Each time series should have a long history, ideally more than 2 years if trying to capture annual events, and each time series more than 300, ideally at least 1K data points. | Amazon Forecast's proprietary deep learning DeepAR+, CNN-QR  |
| Small dataset with 1-100's of time series, where majority of time series have more than 300 data points + seasonal effects + related data. | Prophet                                                      |
| Small dataset with 1-10's of time series, where majority of time series have more than 300 data points + seasonal effects. | ETS, ARIMA                                                   |
| Intermittent (sparse containing many 0s) with 1-10's of time series, where majority of time series have more than 300 data points. | Amazon Forecast's proprietary NPTS                           |
| Small dataset (regular or sparse) with 1-10's of time series, where majority of time series have fewer than 300 data points. | The data is too small for Amazon Forecast. Try ETS in Excel or the traditional statistical models ARIMA, Prophet instead. |



<a name="mapping"/>

### Mapping your data into time series

- Historical sales data is called the **Target Time Series (TTS)**.  This is the minimum data required to do forecasting.  It consists of 
  - An **"item_id", or some unique identifier, for the things you want to forecas**t.  The unique identifier is sometimes a concatenation of item_id and location_id.  Or sometimes it is even more fields concatenated together to form a unique time series identifier.
  - Also a **"timestamp" when the sale occurred**
  - And a **"target_value" or sales quantity**
- In addition to historical sales data, **sometimes other data is known per item at exactly the same time as every sale.  This is called the Related Time Series (RTS)**.  Related data can give more clues to what future predictions could look like.  The best related data is also known in the future.  For example Prices, Promotions, Economic indicators, Holidays, sometimes even Weather.
- Especially for cold-starts, or new product introductions, it is important to have Item Metadata (IM).  **Item Metadata is static information with respect to time, it varies only per fixed "item_id"**.  Examples of metadata are type of item, product group, genre, color, class.



### Data Prep Best Practices<a name="dataprep"/>

If you are a developer or line of business person reading this, you are our target audience!  However, a small amount of "Data Thinking" or Data Science is required.  Machine learning models are only as good as the data put into them.  For this reason, we have a whole section dedicated to Data Prep and the reasoning behind that.  Common things to watch out for are missing timestamps or missing "item IDs", having 0's when in fact those values are missing, uniqueness of sales by item by timestamp (aggregation level), and extreme values.  "Dirty data" can affect the accuracy of Forecast models.

In terms of data, Forecasting works best on "dense" data. When, per timestamp and "item" to forecast, there is almost always a data point.  Examples of dense data include high-volume transactional consumer demand, call center demand, IT infrastructure demand, location-based service needs, electricity use.  "Sparse" data is when per timestamp and item very few sales happen.  Examples of sparse data are when the SKU is so targeted that it does not sell frequently, sales order data, or financial revenue numbers that are summarized per month.  Sparse data is difficult to forecast because as a time series there is not enough of it to establish a pattern.  Time series patterns are used to predict when and with what amplitude a particular "item target value" will occur in the future.  

For additional best practices and recommendations on data preparation, focused on sales and demand planning, but also generally applicable, refer to the [Amazon Forecast Data Set Guidance for Sales and Demand Planning](./ForecastDatasetGuidanceSales.md).


**Developers:**  [Use AWS Glue DataBrew](https://aws.amazon.com/glue/features/databrew/), a data preparation UI tool, to clean data and save TTS to S3.  TODO link 5min video<br />

**Data Scientists:** We have DataPrep Jupyter notebook templates.  We have included common data prep steps we have noticed in customers' data.  

- If data is Hourly or below - [use the regular DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb)
- If data is Daily or Weekly - [use the weekly DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi_weekly.ipynb) <br />



## Getting Started with Amazon Forecast Best Practices and Tutorial<a name="bestpractice"/>

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

​			Rule: Forecast length cannot be longer than 1/3 of training data 

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

​		 “yyyy-MM-dd” if DataFrequency is Daily or higher, see [documentation](https://docs.aws.amazon.com/forecast/latest/dg/API_CreatePredictor.html)

8) **Pay special attention to gaps or 0’s in your data. Pro tip: convert all 0’s to nulls,** then let Amazon Forecast do automatic null-filling through its Featurization settings.  See [the null-filling syntax](https://docs.aws.amazon.com/forecast/latest/dg/howitworks-missing-values.html).

- If you're forecasting product demand for a retail store and an item is sold out or unavailable, there would be no sales data to record while that item is out of stock. We recommend that you fill the gaps in the historic sales data or target time series with NaN instead of 0. Filling with 0, the model might learn wrongly to bias forecasts toward 0. 
- **Differentiate between out of stock and end of life**.  You may want to either fill missing values differently or have separate related time series for end of life products/dates and stock-outs by products/dates. 

9) **Create training subset of sample data, with hold-out of 1 forecast length.** So training data is all sample data except last data points in time series of length forecast length. Reserve the hold-out data for forecast evaluation.

Note: the forecast hold-out data is for developing custom error/accuracy metrics that can be calculated on exported forecasts, if desired.  If no custom metrics are required, there is no need for the hold-out, all the data can be used for training.  [Errors/accuracy are automatically calculated by Amazon Forecast system on forecasts using the "backtest technique".](https://docs.aws.amazon.com/forecast/latest/dg/metrics.html)  

**Note: special consideration for cold-start or new product introductions**.<a name="coldstart"/>  For best results, do not include new items in your training data.  Do include new items in the inference data.  If fewer than 5 data points exist per new item, be sure to fill missing values explicitly for the new items with "NaN"; otherwise the cold-start items will be silently dropped.  For training, keep the [default null-filling frontfill= "none"](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#null-filling).

**Above new items advice assumes new items are the exception** and you have a majority set of "core" items with long histories.  For some customers, their items are almost all short-lived, so at any point in time, items are mostly either new or near end-of-life.  In this case, try to see if you have a higher-level item group that represents "substitution items" grouping.  Can you build a model at this substitution item_grouping level?  Otherwise, the only other option is to try the Deep Learning algorithms with metadata that ties together items, which may be in various phases of their life cycles, and are all included in the training data.

10) **Create just historical sales part of training data (TTS).** Subset out just the timestamp, item_id, target_value columns.  Save this TTS subset of training data on S3, example as TTS.csv.  

Copy the "S3 URI" to TTS.csv

<a name="tutorial"/>

## Tutorial to get your first Predictor  

Best Practices are continued inside this tutorial.

11. **If you haven't already, [create an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)**

12. **Login to your AWS account and navigate to Forecast**
    console.aws.amazon.com > Type forecast in the search bar > click on Amazon Forecast

13. **Create a Dataset Group and Target Time Series data**
    1. On the Forecast console, click Create dataset group

    2. Give your Dataset Group a name, and choose Custom “domain” or another vocabulary for convenience, it makes no difference to forecast algorithms whether you call your target value “demand” or “target_value”, the column headers will be dropped anyway. 

    3. Click Next

    4. Give your TTS dataset a name, choose data frequency, e.g. “D”. This should match [Step 3.3 above](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice).

    5. Use the default schema builder to drag columns in the same order as your TTS data from [Step 10 above](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice). 

    6. Make sure the schema timestamp format matches your choice from [Step 7 above](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice)

    7. On Dataset import details, paste the S3 URI location of TTS.csv from [Step 10 above](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice). 

       > Alternatively, you can [use our taxi demo data](https://amazon-forecast-samples.s3.amazonaws.com/automation_solution/demo-nyctaxi/nyctaxi_weather_auto.csv).  Download it locally, upload to S3, copy the S3 URI.

    8. Click Start

14. **Wait the specified time, then check your Dataset import field statistics.** 
    1. Make sure the data import statistics look right.
    2. \# of expected items, # locations, time range, other fields all look correct?
    3. If any of above does not look right, [return to Data Prep best practices and try again](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice).

15. **Choose probabilistic quantiles that fit your business goals.**  The optimal choice of quantile reflects the average proportion between marginal profit and the production and inventory holding costs.  In other words, the quantile choice should be based on the lost opportunity cost of under-forecasting and the cost of over-producing and holding over-forecasted items.  

    - The risk tolerance for certain SKUs might be higher than others. For long shelf life items, you may prefer to overstock because you can easily store excess inventory. For items with a short shelf life, you may prefer a lower stocking level to reduce waste. **It’s ideal to train one model but assess forecasting accuracy for different SKUs at different stocking levels.**
    
    - For some items the opportunity cost dictates decisions.  For example, a p90 forecast is useful when you have something like milk or toilet paper, that a grocery store never wnats to run out of and doesn't mind always having some remaining on the shelves. On the other hand, for an expensive machine, a p10 forecast would be more useful since you don’t want to carry such expensive inventory costs and customers probably aren’t expecting that machine to just be sitting around in stock anyway. As an extreme example, Amazon Redshift uses Forecast at p99 levels, because they never want to run out of virtual resources. [See documentation for more details on metrics.](https://docs.aws.amazon.com/forecast/latest/dg/metrics.html)
    
      
    
    > **If you don't know your business costs of under- vs over- forecasting, or maybe such costs are equal, use the default values for AutoML which are p10, p50, p90.**  
    
    - Typically forecasters choose 3 quantiles.  For example, generating 3 forecasts at p10, p50, p90 results in an 80% confidence interval around the p50 forecast.  When making charts, typically the region between p10 and p90 is shaded to indicate the 80% confidence interval.


    - Note:  In the predictor output, errors for each quantile forecast are called "wQL" or weighted quantile loss, which is the error of that quantile forecast. 


    > Technical details:  The formal definition of a quantile forecast is Pr(actual value <= forecast at quantile q) = q.  Technically a quantile is a percentile/100.  Statisticians tend to say ”p90 quantile-level“, since that is easier to say than "“quantile 0.9”. For example, a p90 quantile-level forecast means the actual value can be expected to be less than the forecast 90% of the time.  Specifically if at time=t1 and quantile-level=0.9, the predicted value = 30, that means the actual value at time= t1, if you had 1000 simulations, would be expected to be less than 30 for 900 simulations, and for 100 simulations, the actual value is expected to be over 30.

16. **Training Strategy: Start simple with historical sales data only (TTS) and AutoML.  Iterate just on this data before adding Meta- and Related data.**  This will give you a baseline, so you will be able to determine which data and/or training iterations are working to improving accuracy.  

    AutoML will automatically run through all 6 algorithms, (the DL algos will run with HPO turned on), to learn which algorithm works best on your data. This will take a long time the very first time. But, you will get understanding which algorithm fits best to your data.  [See algorithms section of documentation](https://docs.aws.amazon.com/forecast/latest/dg/aws-forecast-choosing-recipes.html). 

    AutoML calculates the average of the weighted P10, P50 and P90 quantile losses (or your own quantiles instead of default quantiles), and [will return the algorithm with the lowest averaged value](https://docs.aws.amazon.com/forecast/latest/dg/howitworks-predictor.html).

17. In the navigation pane, under your dataset group, choose **Predictors**.

18. Choose **Train** **predictor**.  Train using AutoML

    1. Click Train new predictor

    2. Give your predictor a name. 

    3. Choose Forecast horizon [from Step 3.2](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice). 

    4. Choose Forecast frequency [from Step 3.1](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice).

    5. Under Predictor details > Algorithm > Select radio button for Automatic (AutoML) 

    6. Choose number of backtest windows = 3.  Max number: 5.  

       **Best practice:  always choose more than 1 backtest window.**  

       

       ![](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/backtest_windows.png)

       

       - [Forecast uses backtesting](https://docs.aws.amazon.com/forecast/latest/dg/metrics.html) to tune predictors and produce accuracy metrics. To perform backtesting, Forecast automatically splits your time-series datasets into two sets: training and testing. The training set is used to train your model, and the testing set to evaluate the model’s predictive accuracy. **We recommend choosing more than one backtest window to minimize selection bias**, in case one window is more or less accurate by chance. **Assessing the overall model accuracy from multiple backtest windows provides a better measure of the strength of the model and reduces the chance of overfitting.** 

       

    7. **Expand the “Advanced configurations” and scroll down to the "Featurizations"** section to view null-filling options.<a name="null-filling"/>

    ![](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/understandNullFilling.png)

    - **Pro-tip: convert all 0's to nulls and let Amazon Forecast do the heavy lifting of automatically imputing missing values**.  Amazon Forecast will automatically detect whether the missing values occur due to new product introduction (cold-starts) or end-of-life products.  

    - You can use several missing value logics including value, median, min, max, zero, mean, and nan (target time series only), depending on the specific use case. 

    - [Null-filling featurization terminology and syntax](https://docs.aws.amazon.com/forecast/latest/dg/howitworks-missing-values.html):

      - "**frontfill**" - (TTS only) refers to new (cold-start) items and how you want to treat nulls before the item begins to have any history
      - "**middlefill**" - refers to nulls in the middle of time series values
      - "**backfill**" - refers to end-of-life items and how you want to treat nulls after an item has stopped selling
      - "**futurefill**" - (RTS only) refers to nulls that occur after the end of training data

    - **If the default filling looks fine, you don’t need to do anything**

    - Below is a JSON example if you want to change middlefill=”zero” (everything between 1st and last timestamps) and backfill=”nan” because you know you have some products with end-of-life, paste the sample JSON below.

      ```json
      [
      	{
    		"AttributeName": "target_value",
      		"FeaturizationPipeline": [
    			{
      				"FeaturizationMethodName": "filling",
    				"FeaturizationMethodParameters": {
      					"aggregation": "sum",
    					"frontfill": "none",
      					"middlefill": "zero",
    					"backfill": "nan"
      				}
    			}
      		]
    	}
      ]
      ```

    8. **Click Start**

19. **Wait the specified time, then check each AutoML predictor results**

    - Choose your predictor on the **Predictors** page to view the details.

    - **Check each predictor from AutoML, look if any errors**
      - Check the “Items” column. Is that the full # time series? If not, why? 
      - Do you have enough history to support the desired forecast length? 
        - If not, you’ll get an error message. 
        - **Rule: Amazon Forecast requires length of forecast to be shorter than 1/3 of training data.**
      - Do you have enough data per time series? 
        - If not, you’ll get error message. E.g. Very low # of observations (found 238 observations in 3 time series). 
        - **Rule: Deep Learning algorithms require at least 300 observations in the majority of time series.**
        - One way to fix this error is aggregate at higher levels of granularity:
          - Can you aggregate to higher time dimension? E.g. Instead of Hourly, try Daily?  
          - Can you aggregate to higher item/location dimension? E.g. Instead of SKU, try product group level? 
          - Return to Best Practice Data Prep for suggestions
      - Repeat all steps up to here until you pass all error-checks

20. **Choose your AutoML winning predictor on the Predictors page to view the details.**
    ![](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/understandPredictorResults.png)

    - Check the **Predictor metrics** section.  
      - Top row is average of below rows. 
        
        - Each row below is metrics per backtest window 
        
      - Columns are: type, start, end , #Items found per backtest window, and metrics including:
        - Each quantile’s weighted quantile error (lower is better).  Up to 5 quantiles.
        - WAPE (measured at mean, which may be different from p50 quantile). 
  - RMSE (measured at mean, which may be different from p50 quantile).
    
      - As [explained in Step 15](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#tutorial), Amazon Forecast generates a forecast at a particular quantile. Weighted quantile loss is the error metric or “wQL”. Machine learning models work by minimizing (or maximizing) an objective function, in this case loss or prediction error. The weighted quantile loss function is weighted to penalize forecast values at kth percentile that are higher than actuals more when k < 0.5 and the reverse when k > 0.5. So, p10 quantile predictions that are higher than actuals will get 0.9 weightings; whereas p90 quantile predictions that are lower than actual will get 0.9 weighting. The full formula is:
    ![](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/Formula_wql.png) 
    
    [See documentation for more details.](https://docs.aws.amazon.com/forecast/latest/dg/metrics.html.)
21. **Save a record of your experiments in Excel (or some place local):**  

    This will make it easier to compare future experiments to be able to tell what is working.  
    ![](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/Experiments_excel.png)



22. Remember,  [from Step 1 from Best Practice](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice), Improving forecast accuracy for specific items—such as those with higher prices or higher costs—is often more important than optimizing for all items.  By exporting the Predictor backtest exports, item-level accuracy can be calculate for specific items or groups of items, without needing a hold-out data set.  [See our notebook for an example of custom item-level metrics from Predictor backtest exports](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Item_Level_Accuracy/Item_Level_Accuracy_Using_Bike_Example.ipynb).

<br>

## Iterating Models and What-if Best Practices<a name="iteratebp"/>

23. **Sequentially experiment.**  It may be tempting to run many experiments in parallel at the same time.   But this will prevent you from learning from previous jobs, and in the process, you may miss an experiment that would have worked. 

    **As you experiment, it is best to keep the same Quantile choices.**  This is why it is crucial to clarify the Business Requirements up front.  Recommended metrics to determine winning experiments are:

    	1. Lowest average over all wQLs.  If tie, then:
    	2. Lowest WAPE.  If tie, then: 
    	3. Lowest RMSE. 

    As a developer or Business leader, here you need to think a little bit like a Data Scientist.  A good model, quite often, does not happen on the first try.   Machine learning models are only as good as the data put into them, so the data itself very likely may need improvement.  

24. As [mentioned in Step 16](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#tutorial), **the best strategy is to:** 
    1. **start simple with just historical data (TTS) and AutoML.**  From there, you will find out which is the best algorithm for your data.  
    2. **For all future experiments, stick to this same algorithm, then use HPO=True.**  AutoML mode did a light HPO, to verify which algorithm is best, but the parameter optimization is not as deep as explicitly setting HPO toggled on for a single algorithm.
    3. Finally, when you have finished iterating,  **use the fixed algorithm and fixed Training Parameters from the last HPO Predictor.**

25. **Iterating and scaling to value.**  Unlike Machine Learning Competitions, real life POCs are not about "highest accuracy at any cost".  In real life, there is often a balance to think about:  Accuracy, Scaleability, Effort.  Since human time is expensive, there might be other activities of more value than trying to get the utmost extra amounts of accuracy out of Forecast models.

Keeping this in mind, some typical next iterations, in order of easiest-to-hardest and most-to-least expected incremental accuracy improvements: 
<br>

- **Try different null-value featurizations.**  Easy if you followed our Pro tip in Best Practices, and converted all 0’s to nulls.  You can do this on same dataset, just train new Predictor with different featurization choices. [See documentation for syntax](https://docs.aws.amazon.com/forecast/latest/dg/howitworks-missing-values.html).

- **Subset data in different ways and try training a separate model per subset.**  Difficult - you'll have to import each dataset separately, train a Predictor per data subset.  Compare identical item accuracies across subset model vs global all-in model.

  - For example Python functions to split data by top-moving, dense-only, or erratic-only,  [see our example DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb)
  - For example Python functions to calculate item-level metrics for subset groups of items using the Predictor backtest export, [see our example Item_Level_Accuracy notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Item_Level_Accuracy/Item_Level_Accuracy_Using_Bike_Example.ipynb). 

  Below is an example Amazon QuickSight visualization, comparing the same random items across 3 models:  1) top row is global all-in model that was trained on all data at once; 2) 2nd row is same items from model trained on subset only "top-moving" items; 3) 3rd row is same items from model trained on subset only "erratic time series"  items.  We can see below that items from the Erratic-only model have highest accuracy.  On the other hand, we expect the subset of items that are not-erratic or not-top-moving, which are harder to forecast, will have better accuracy when taken from the top, all-in model.
  <img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/quicksight-example-model-iterations.png" alt="Compare models created on different data subsets" style="zoom:70%;" />

- **If using DeepAR+ algorithm, try a different likelihood function.  Easy.**  The default likelihood function "student-t" works best most of the time.  Plot the target-value histogram and see which distribution the plot looks like.  Use these general rules based on what you see:

  - Positive counting numbers -> Use negative-binomial

  - Limited range 0 or 1 target_value -> Use beta
  
  - Floating point decimal numbers -> Usually student-t; very rarely gaussian
    - Use student-t when any of: population size is small, or population standard deviation unknown, or you expect heavier tails than “normal”
  - Non-stationary Poisson, or different student-t’s in different time ranges (e.g. higher traffic during commuting hours) -> Try piecewise-linear 
  - PW-linear likelihood function wins - for irregular data - e.g. web traffic, retail sales
  - Student-t  wins for regular data - e.g. electricity, highway traffic 

- **Use the built-in, AWS-hosted data enrichments: Holidays and Weather.  Easy.**  Both of these variables can help more accurately predict sales.  Weather requires daily (or lower) time granularity of data, forecast horizon <= 14 days, and up to 2K geolocations per model.  Weather also requires locations to be more than just string names, that is, to have actual geolocations.  Geolocations can be 2-digit country code + "_" + 5-digit zip or actual latitude_longitude.  https://docs.aws.amazon.com/forecast/latest/dg/weather.html

  - When you train a Predictor with either Holidays and/or Weather features enabled, use HPO=True, or Hyperparameter Optimization toggled on, so you get the best tuned Predictor.  Make sure you do this before making inferences (or forecasts).

- **Add Item Metadata (IM) and/or Related (RTS) data.  Difficult.**  For RTS, the first time you'll have to figure out the best featurization and import the data.  To decide which data to use as a related time series start with:

  - Discuss with your business users to build an intuition of what factors might impact your product demand. 

  - Visualize the data by overlaying it with your target time series to see patterns.   

    - For example below, we visualize a candidate "weekend" related time series feature by overlaying the 0-1 variable (red) with actual values.
      <img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/visualize_related_weekend.png" style="zoom:50%;" />

  - Assess correlation between the target_value and the related variable

  - Try transformations - e.g. log(price) instead of abs(price)

  - Try related time series one at a time and trying in different combinations. Sometimes you might have to transform your related time series data to see if the accuracy increases. 

  - **Pro-tip:  Train a new Predictor using just CNN-QR**, if possible, so you can tell from the Predictor parameters if the new data gets picked up or not.  Inside the Predictor Training Parameters, you want to see: 

    ```json
    "use_related_data": "ALL",
    "use_item_metadata": "ALL",
    ```

  - If CNN-QR is not using all your IM and RTS, it means your data was not found to be useful.  Time to iterate on the data.

  - Prophet is the only statistical algorithm that can use RTS; it cannot use Item Metadata.

  - To use both IM and RTS, you will need to use a Deep Learning Algorithm

  - **If you are trying to forecast "cold-starts" or new products, Item Metadata is required.**  Provide item group names to tie together new products with existing products with longer histories.  Forecasting cold-starts can only be done using Deep Learning algorithms.

  - To iterate on IM and RTS, it is possible to change the data and perform inference-only.  See Running an experiment without re-training by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/WhatIf_Analysis/WhatIf_Analysis.ipynb. At the moment, forecast metrics are not automatically calculated, so this approach takes a lot more effort, and may not end up saving you time between iterations.  

- **To get the best accuracy, once you have finalized the IM and RTS fields, train with HPO=True**, or Hyperparameter Optimization toggled on, so you get the best tuned Predictor.  Make sure you do this before making inferences (or forecasts).  At the moment, since Predictor metrics are automatically calculated, re-training each experiment with HPO=True, might be the most efficient approach, since your time is not completely occupied and can be spent somewhere else during training times.

 

<br>

## Generating Forecasts<a name="forecastinference"/>

Choose whether to generate forecast using the same train data or whether to update data.  

- If using same data used for training, then the forecast will be generated past the end of the train data, extending one forecast horizon out into the future.  If you kept a hold-out, this data can be used to manually verify the generated forecast after you export it and save it to S3 (as in Step 31).

- It is also possible to import updated data into the DataSet Group to which your final Predictor belongs.  This would happen typically when re-training is not required, but new inferences are needed.

  - Example:  Company A generates weekly forecasts, but models only need to be retrained seasonally, once per quarter.  This means each week, company A imports new data, bringing in the latest data available, before generating a new forecast.  The first week of each quarter, Company A would perform a complete retraining of their forecast model, before generating that week's forecast.

  - Note:  Cold start items must be included as updated data.  Notice that there is a system constraint such that at least 5 data points need to exist per time series. Therefore, for the item that has less than 5 observations, be sure to encode target_value as Float and fill explicitly with "NaN".  

    Note: Cold-start forecasting only works if new items are tied to items with longer histories through Item Metadata.  

30. **Create a Forecast**

31. **Select a Predictor** (will automatically use latest imported data in DataSet Group to which Predictor belongs)

2. **Choose forecast types (quantiles)** 
   
   1. Pro-tip.  For fastest imputations. choose same quantiles you chose for Predictor.  The reason for this is that all algorithms, except DeepAR+, will have to do extra simulations to re-calculate if the quantiles are different between how model was trained and how forecasts will be imputed.
   
33. Click Start.

34. **Export a Forecast**

35. Under the **Exports** section, **click Create forecast export**

36. Give the export a name

37. In the S3 forecast export location, paste an S3 path to your own location to save.

    Note: any kind of Amazon Forecast Delete action - Hierarchical delete, or any individual delete action will not delete your exported, saved forecast copy.

    Note: In the downloaded forecast .csv file, probabilistic quantile-level forecasts are indicated by named column, for example "p90"  for the  "p90 quantile-level forecast".

38. **Query a Forecast**

    1. **Wait the specified time, then select Forecast lookup**

    2. Pro-tip:  Look at you Dataset Import page to recall the last possible time stamp of the end of the forecast horizon.  **Enter this as "End date".** 

       Forecast service reserves a fixed amount of memory, so the "Start date" varies depending on your particular data size.  **Work backward from End date to figure out the best "Start date".**

    1. **Per time series dimension, add them using "Add forecast key"**
    2. **Enter value for an item you want to look up.** Add values per forecast dimension if you have extra dimensions.
    3. **Click "Get Forecast"**



## Example Notebooks<a name="notebooks"/>

1. Getting started with API calls:  https://github.com/aws-samples/amazon-forecast-samples/tree/master/notebooks/basic/Tutorial
4. Evaluating your predictor using backtest item-level forecasts by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Item_Level_Accuracy/Item_Level_Accuracy_Using_Bike_Example.ipynb
5. Running an experiment without re-training by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/WhatIf_Analysis/WhatIf_Analysis.ipynb
6. Adding built-in AWS-hosted weather data by API call:  https://github.com/aws-samples/amazon-forecast-samples/tree/master/notebooks/advanced/Weather_index
5. Adding Related data by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Incorporating_Related_Time_Series_dataset_to_your_Predictor/Incorporating_Related_Time_Series_dataset_to_your_Predictor.ipynb
6. Adding Metadata by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Incorporating_Item_Metadata_Dataset_to_your_Predictor/Incorporating_Item_Metadata_Dataset_to_your_Predictor.ipynb
7. Forecasting "cold-start" or new product introductions by generating test data explicitly filled with "NaN" for new items and running Forecast-only (that is inference only) using already trained predictor by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Forecast%20with%20Cold%20Start%20Items/Forecast%20with%20Cold%20Start%20Items.ipynb

<br>

## Demos/Workshops<a name="workshops"/>

- **[Pre-POC workshop](https://github.com/aws-samples/amazon-forecast-samples/tree/master/workshops/pre_POC_workshop)** is a hands-on, leave-in-place, guided learning (and demo) that is meant to accelerate a Forecast POC.  The workshop covers Best Practices for working with Amazon Forecast.  Targeted to Developers, Line-of-business, and Data Scientists who will be doing the execution work of a Forecast POC.  
  - Data used:  NYC Taxi
  - Tools used:  
    - [Getting Started Guide and Best Practices Cheat Sheet Tutorial](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md)
    - [Improving Forecast Accuracy with Machine Learning Solution](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/install-forecast-solution.md)
- **No code workshop** can be used in 2 ways:
  - [**Introduction demo**](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/no_code_workshop/forecast-with-console.md).  Developers and Line-of-business folks can follow-along this markdown file to learn start-to-finish how to create forecasts.  100% no-code, through UI screens using console only.  
  - **[Notebook using Amazon Forecast Python SDK](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/no_code_workshop/forecast-with-api-completed.ipynb)** to make API calls to perform exactly the same tasks as the 100% no-code demo.  Targeted at Integration Partners, MLOps Engineers, and Developers responsible for putting forecasts into production.
  - Data used:  Energy consumption
- Immersion Day Workshop is an older version of the No code workshop notebook portion.



## Videos<a name="videos">

- High-level intro to Amazon Forecast (minutes 1-8), demo (minutes 8-18), and customer story in retail (minutes 20-34): https://www.youtube.com/watch?v=K7MaDbn8_l0
- TODO: Demo how to prepare data for Amazon Forecast using AWS Glue DataBrew (5min) : 
- [Demo video](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/demo_videos/video_import_console.mp4) how to import data using Amazon Forecast screens for NYC taxi data (6min):
- [Demo video](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/demo_videos/video_train_eval_console.mp4) how to train (minutes 1-2:30) and evaluate a predictor (minutes 2:30-6) using Amazon Forecast screens for NYC taxi data (6min):
- [Demo video](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/demo_videos/video_create_query_vis_forecast.mp4) how to create a forecast, query forecast in console, and visualize through Amazon Quicksight BI Dashboard (2min):
- TODO: Demo how to train a predictor using Improving Forecast Accuracy with ML Solution CloudFormation template (5min):



## More Resources<a name="moreresources"/>

- Links for Amazon Forecast

- - [Documentation page:  ](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html)https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html 

  - Whitepaper:  https://d1.awsstatic.com/whitepapers/time-series-forecasting-principles-amazon-forecast.pdf

  - Customer references: https://aws.amazon.com/forecast/customers/

  - Qualified partners: https://aws.amazon.com/forecast/partners/

  - Automation pipeline solution:  https://aws.amazon.com/solutions/implementations/improving-forecast-accuracy-with-machine-learning/?did=sl_card&trk=sl_card

  - Github tutorials:  https://github.com/aws-samples/amazon-forecast-samples/tree/master/workshops 

  - Blogs: https://aws.amazon.com/blogs/machine-learning/category/artificial-intelligence/amazon-forecast/

  - - SAP-Forecast integration: https://aws.amazon.com/blogs/awsforsap/sales-forecasting-in-sap-with-amazon-forecast/

- Amazon Forecast Science:

- - Tutorial for time series forecasting with video: https://lovvge.github.io/Forecasting-Tutorial-WWW-2020/
  - https://www.amazon.science/videos-and-tutorials/forecasting-big-time-series-theory-and-practice
  - DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks- 2017. https://arxiv.org/pdf/1704.04110.pdf
  - CNN-QR: A Multi-Horizon Quantile Recurrent Forecaster -2018. https://arxiv.org/pdf/1711.11053.pdf 
  - Intermittent Demand Forecasting with Renewal Processes - 2020. https://arxiv.org/pdf/2010.01550.pdf
  
- AWS AI Science Forecasting book:  https://www.amazon.com/Business-Forecasting-Emerging-Artificial-Intelligence/dp/1119782473