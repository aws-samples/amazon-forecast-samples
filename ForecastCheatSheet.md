# Amazon Forecast Cheat Sheet

##### Table of Contents  
* [Intro: Is Amazon Forecast a Good Fit?](#intro)  
* [Getting Started Best Practices](#bestpractice)  
* [Iterating Models What-if Best Practices](#iteratebp)
* [Getting Started Tutorial](#tutorial)
* [Example Notebooks](#notebooks)
* [Demos/Workshops](#workshops)
* [More Resources](#moreresources)

<a name="intro"/>
Amazon Forecast offers as a product, the same deep learning probabilistic forecast technology developed at Amazon (which offers over 400million different products and ships Billions of packages in 185 different countries every day).  Amazon Forecast addresses the challenge of more accurate forecasting as a fully managed service.  Users do not need to be machine learning experts in order to achieve accuracy levels that used to take months of engineering. <br>
<br>
For more information, see our documentation: https://docs.aws.amazon.com/forecast/latest/dg/getting-started.html


## Intro:  Is Amazon Forecast a Good Fit?

Not all machine learning problems are forecasting problems.  The first question to ask is "Are time series involved?"  For example, do you need a particular value only at a particular time and date in the future?  Forecasting is not a good fit for general, static (where the particular date/time does not matter) problems, such as fraud detection or recommended movie titles to users.  There are much quicker solutions to static problems.  

If you are a developer or line of business person reading this, you are our target audience!  However, a small amount of "Data Thinking" or Data Science is required.  Machine learning models are only as good as the data put into them.  For this reason, we have a whole section dedicated to Data Prep and the reasoning behind that.  Common things to watch out for are missing timestamps or missing "item IDs", having 0's when in fact those values are missing, uniqueness of sales by item by timestamp (aggregation level), and extreme values.  "Dirty data" can affect the accuracy of Forecast models.

In terms of data, Forecasting works best on "dense" data. When, per timestamp and "item" to forecast, there is almost always a data point.  Examples of dense data include high-volume transactional consumer demand, call center demand, IT infrastructure demand, location-based service needs, electricity use.  "Sparse" data is when per timestamp and item very few sales happen.  Examples of sparse data are when the SKU is so targeted that it does not sell frequently, sales order data, or financial revenue numbers that are summarized per month.  Sparse data is difficult to forecast because as a time series there is not enough of it to establish a pattern.  Time series patterns are used to predict when and with what amplitude a particular "item target value" will occur in the future.  

Amazon Forecast's strength is its deep learning algorithms.  Traditional statistical methods, sometimes called "local models", are able to learn one time series at a time.  That means if you have 20K items to forecast, then 20K traditional models are required; each model unable to learn from other models.  Traditional statistical algorithms include:  Exponential Smoothing (ETS), ARIMA, NPTS, and Prophet.  These traditional algorithms are included in Amazon Forecast.

Deep learning algorithms, sometimes called "global models", are able to learn using more than 1 time series at a time.  That means if you have 20K items to forecast, and they have interrelationships between them such as item-affinity or cannibalism, such behaviors can be learned by inputting them all into a single model.  Amazon Forecast's proprietary deep learning algorithms include:  DeepAR+ (an LSTM version of RNN) and CNN-QR (a quantile regression version of CNN, a neural network topology typically used in computer vision). 

The historical sales data is called the Target Time Series (TTS).  This is the minimum data required to do forecasting.  In addition to historical sales data, sometimes other data is known per item at exactly the same time as every sale.  This is called Related Time Series (RTS) data.  Related data can sometimes give more clues to what future predictions could look like.  The best related data is also known in the future.  For example Prices, Promotions, Economic indicators, Holidays, sometimes even Weather.

All of this is summarized in the following table:

| Criteria                                                     | Amazon Forecast Algorithm class                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Large dataset with up to 1 million time series with similar underlying patterns + seasonal effects + related data. Each time series should have a long history, ideally more than 2 years if hoping to capture annual events, and each time series more than 300, ideally at least 1K data points. | Amazon Forecast's proprietary deep learning DeepAR+, CNN-QR  |
| Small dataset with 1-100's of time series, where majority of time series have more than 300 data points + seasonal effects + related data. | Prophet                                                      |
| Small dataset with 1-100's of time series, where majority of time series have more than 300 data points + seasonal effects. | ETS, ARIMA                                                   |
| Intermittent (sparse containing many 0s) with 1-100's of time series, where majority of time series have more than 300 data points. | Amazon Forecast's proprietary NPTS                           |
| Small dataset (regular or sparse) with 1-100's of time series, where majority of time series have fewer than 300 data points. | The data is too small for Amazon Forecast. Try ETS in Excel or the traditional statistical models ARIMA, Prophet instead. |



## Getting Started Best Practices<a name="bestpractice"/>

Following are Best Practices.  Make sure you know how success is measured, i.e. metric that matters.  Start simple with historical sales data only (TTS) and AutoML feature, to learn which algorithm works best on your data.  This way you'll have a baseline, and be able to iterate more efficiently.   

AutoML will automatically run through all 6 algorithms, (the DL algos will run with HPO turned on), to learn which algorithm works best on your data. This will take a long time. But, you will get understanding which algorithm fits best to your data.  See https://docs.aws.amazon.com/forecast/latest/dg/aws-forecast-choosing-recipes.html. AutoML calculates the average of the weighted P10, P50 and P90 quantile losses (or your own quantiles instead of default quantiles), and returns the algorithm with the lowest averaged value https://docs.aws.amazon.com/forecast/latest/dg/howitworks-predictor.html

1. **Pre-segmentation of data, call this your sample data.** For example, most data follows approx 80/20 rule, where 20% of the items are top-selling; the rest 80% of items are low-volume long-tail. **A good first sample is the 20% dense time series sample.**

2. **Decisions:**

   2.1 **What is your forecast time unit granularity?** For example, if you want to predict with weekly granularity, answer = “W”.

   ​	Choices are: Y|M|W|D|H|30min|15min|10min|5min|1min

   2.2 **How many time units do you want to forecast? Call this forecast length.** For example, if your time unit is Hour, then if you want to forecast out 1 week, that would be 24*7 = 168 hours, so forecast length = 168.

   ​	Rule: Forecast length cannot be longer than 1/3 of training data 

   2.3 **What is the time granularity for your data?**. For example, if your time unit is Hour, answer = "H".  

   ​	Choices are: Y|M|W|D|H|30min|15min|10min|5min|1min

   ​	Usually the same as forecast granularity. 

   ​	**Rule: Data granularity can be <= forecast granularity.**

   2.4 **Identify unique dimensions of what you want to forecast (time series). Adjust your aggregation and timestamps if necessary.**

3. **Identify columns in your data that you will map to: timestamp, item_id, target_value**

4. Possibly, but not required right away, identify other data you think in future might help inform forecasts – example Prices, Promotions, Stock-out dates, Holidays.

5. **Check for uniqueness.**  When you groupby timestamp (at identified time unit from Step 2.3 above) and item_id, you should see only 1 target_value. If you see more than 1 target value per timestamp/item_id combination, that means your dimensions aren’t unique for your data. Maybe you have another dimension such as sales location?

6. **Check your timestamp format**, https://docs.aws.amazon.com/forecast/latest/dg/API_CreatePredictor.html 

   e.g. “yyyy-MM-dd” if DataFrequency is Daily or higher, see

7. **Pay special attention to gaps or 0’s in your data.** Pro tip: convert all 0’s to nulls, then let Amazon Forecast do automatic null-filling through its Featurization settings.  https://docs.aws.amazon.com/forecast/latest/dg/howitworks-missing-values.html

8. **Create training subset of sample data, with hold-out of 1 forecast length.** So training data is all sample data except last data points in time series of length forecast length. Reserve the hold-out data for forecast evaluation.

9. **Create just historical sales part of training data (TTS).** Subset out just the timestamp, item_id, target_value columns.  Save this TTS subset of training data on S3, example as TTS.csvCopy the S3 path to TTS.csv
10. Follow tutorial below to get your first Predictor
11. Keep track, maybe in Excel, of your first Predictor's performance metrics.  This will make it easier to be able to tell what is working.  



## Iterating Models What-if Best Practices<a name="iteratebp"/>

Some typical next iterations, in order of easiest-to-hardest and most-to-least expected incremental accuracy improvements: 

- Try different null-value featurizations.  Easiest.  You can do this on same dataset, just train new Predictor.

- Use our built-in, AWS-hosted data enrichments: Holidays and Weather.  Both of these variables can help predict sales.  Weather requires hourly or finer time granularity of data and forecast horizon 14 days or less.  Weather also requires locations to be more than just string names, to have actual geolocations.  Geolocations can be 2-digit country code + "_" + 5-digit zip or actual latitude_longitude.  

- Subset data and try training a separate model per subset.  Harder - you'll have to import each dataset separately, train a Predictor per data subset.  Compare identical item accuracies across subset model vs global all-in model.

  For example Python functions to split data by top-moving or erratic-only, [see our example DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb)

  Below is an example Amazon QuickSight visualization, comparing the same random items across 3 models:  1) top row is global all-in model that was trained on all data at once; 2) 2nd row is same items from model trained on subset only "top-moving" items; 3) 3rd row is same items from model trained on subset only "erratic time series"  items.  We can see below that items from the Erratic-only model have highest accuracy.  On the other hand, we expect the subset of items that are not-erratic or not-top-moving, which are harder to forecast, will have better accuracy when taken from the top, all-in model.
  <img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/quicksight-example-model-iterations.png" alt="Compare models created on different data subsets" style="zoom:70%;" />

- Add Item Metadata (IM) and/or Related (RTS) data.  Hardest - first time you'll have to figure out the best featurization and import the data.  Recommended to train a new Predictor using AutoML so you can tell if the new data gets picked up or not.

  - To iterate on IM and RTS, it's possible to change the data and perform inference-only.  See Running an experiment without re-training by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/WhatIf_Analysis/WhatIf_Analysis.ipynb



## Getting Started Tutorial<a name="tutorial"/>


1. **If you haven't already, create an AWS account**
   https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/

2. **Login to your AWS account and navigate to Forecast**
   console.aws.amazon.com > Type forecast in the search bar > click on Amazon Forecast

3. **Create a Dataset Group and Target Time Series data**
   1. On the Forecast console, click Create dataset group
   2. Give your Dataset Group a name, and choose Custom “domain” or another vocabulary that is convenient for you. The domain is for convenience, it makes no difference to forecast algorithms whether you call your target value “demand” or “target_value”, the column headers will be dropped anyway. 
   3. Click Next
   4. Give your TTS dataset a name, choose data frequency, e.g. “D”. This should match [Step 2.4 above](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice).
   5. Use the default schema builder to drag columns in the same order as your TTS data from [Step 9 above](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice). 
   6. Make sure the schema timestamp format matches your choice from [Step 6 above](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice)
   7. On Dataset import details:
   8. Click Start

4. **Wait the specified time, then check your Dataset import field statistics.** 
   - Make sure the data import statistics look right.
   - \# of expected items, # locations, time range, other fields all look correct?

5. In the navigation pane, under your dataset group, choose **Predictors**.

6. Choose **Train** **predictor**.  Train using AutoML

   1. Click Train new predictor

   2. Give your predictor a name. 

   3. Choose Forecast horizon [from Step 2.2](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice). 

   4. Choose Forecast frequency [from Step 2.1](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice).

   5. Under Predictor details > Algorithm > Select radio button for Automatic (AutoML) 

   6. Choose number of backtest windows = 3

   7. **Expand the “Advanced configurations” section**

      - See https://docs.aws.amazon.com/forecast/latest/dg/howitworks-missing-values.html. Pay attention to the syntax.  Terminology:

        - "frontfill" - refers to cold-start items and how you want to treat nulls before the item begins to have any history
        - "middlefill" - refers to nulls in the middle of time series values
        - "backfill" - refers to end-of-life items and how you want to treat nulls after an item has stopped selling

      - If the default filling looks fine, you don’t need to do anything

      - If you want to change middlefill=”nan” because 0’s aren’t really 0’s and backfill=”nan” because you know you have some products with end-of-life, paste the sample JSON below.

        `[{`

         `"AttributeName": "target_value",`

         `"FeaturizationPipeline": [`

          `{`

          `"FeaturizationMethodName": "filling",`

          `"FeaturizationMethodParameters": {`

           `"aggregation": "sum",`

           `"frontfill": "none",`

           `"middlefill": "nan",`

           `"backfill": "nan"`

          `}`

          `}`

         `]`

        `}]`

   8. Click Start

   9. - - 

7. **Wait the specified time, then check each AutoML predictor for error messages**

8. Choose your predictor on the **Predictors** page to view the details.
   - Check each predictor from AutoML, look if any errors
     - Check the “Items” column. Is that the full # time series? If not, why? 
     - Do you have enough history to support the desired forecast length? 
       - If not, you’ll get an error message. 
       - **Rule: Amazon Forecast requires length of forecast to be shorter of 500 data points or 1/3 of training data.**
     - Do you have enough data per time series? 
       - If not, you’ll get error message. E.g. Very low # of observations (found 238 observations in 3 time series). 
       - **Rule: Deep Learning algorithms require at least 300 observations in the majority of time series.**
       - One way to fix this error is aggregate at higher levels of granularity:
         - Can you aggregate to higher time dimension? E.g. Instead of Hourly, try Daily?  
         - Can you aggregate to higher item/location dimension? E.g. Instead of SKU, try product group level? 
         - Return to Best Practice Data Prep for suggestions
     - Repeat all steps up to here until you pass all error-checks
9. **Choose your AutoML winning predictor on the Predictors page to view the details.**
   - Check the **Predictor metrics** section.  
     - Top row is average of below rows. 
       - Each row below is metrics per backtest window 
       - Each row below is metrics per backtest window 
     - Columns are: type, start, end 
       - #Items found per backtest window 
       - Each quantile’s weighted quantile error (lower is better).  Up to 5 quantiles.
       - WAPE (measured at mean, which may be different from p50 quantile). 
       - RMSE (measured at mean, which may be different from p50 quantile).

10. **Save a record of your experiments in Excel (or someplace local):**

- wQLs (up to 5 quantiles)
- RMSE
- WAPE
- Avg over all wQLs – use this to compare experiments (unless you have different success metric)



## Example Notebooks<a name="notebooks"/>

1. Getting started with API calls:  https://github.com/aws-samples/amazon-forecast-samples/tree/master/notebooks/basic/Tutorial
2. Adding Related data by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Incorporating_Related_Time_Series_dataset_to_your_Predictor/Incorporating_Related_Time_Series_dataset_to_your_Predictor.ipynb
3. Adding Metadata by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Incorporating_Item_Metadata_Dataset_to_your_Predictor/Incorporating_Item_Metadata_Dataset_to_your_Predictor.ipynb
4. Evaluating your predictor using backtest item-level forecasts by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Item_Level_Accuracy/Item_Level_Accuracy_Using_Bike_Example.ipynb
5. Running an experiment without re-training by API call:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/WhatIf_Analysis/WhatIf_Analysis.ipynb
6. Adding built-in AWS-hosted weather data by API call:  https://github.com/aws-samples/amazon-forecast-samples/tree/master/notebooks/advanced/Weather_index



## Demos/Workshops<a name="workshops"/>

- Hands-on leave-in-place tools (and demo) for accelering a Forecast POC:  https://github.com/aws-samples/amazon-forecast-samples/tree/master/workshops/pre_POC_workshop
- Demo of console:  https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/no_code_workshop/forecast-with-console.md
- Demo of API calls:  
  - https://github.com/aws-samples/amazon-forecast-samples/tree/master/workshops/no_code_workshop
  - https://github.com/aws-samples/amazon-forecast-samples/tree/master/workshops/immersion_day



## More Resources<a name="moreresources"/>

- Links for Amazon Forecast

- - [Documentation page:  ](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html)https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html 

  - Whitepaper:  https://d1.awsstatic.com/whitepapers/time-series-forecasting-principles-amazon-forecast.pdf

  - Customer references: https://aws.amazon.com/forecast/customers/

  - Qualified partners: https://aws.amazon.com/forecast/partners/

  - Automation pipeline solution:  https://aws.amazon.com/solutions/implementations/improving-forecast-accuracy-with-machine-learning/?did=sl_card&trk=sl_card

  - Github tutorials:  https://github.com/aws-samples/amazon-forecast-samples/tree/master/notebooks/basic/Tutorial

  - Blogs: https://aws.amazon.com/blogs/machine-learning/category/artificial-intelligence/amazon-forecast/

  - - SAP-Forecast integration: https://aws.amazon.com/blogs/awsforsap/sales-forecasting-in-sap-with-amazon-forecast/

- Amazon Forecast Science:

- - Tutorial for time series forecasting with video: https://lovvge.github.io/Forecasting-Tutorial-WWW-2020/
  - DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks- 2017. https://arxiv.org/pdf/1704.04110.pdf
  - CNN-QR: A Multi-Horizon Quantile Recurrent Forecaster -2018. https://arxiv.org/pdf/1711.11053.pdf 
  - Intermittent Demand Forecasting with Renewal Processes - 2020. https://arxiv.org/pdf/2010.01550.pdf

- AWS AI Science Forecasting book:  https://www.amazon.com/Business-Forecasting-Emerging-Artificial-Intelligence/dp/1119782473
