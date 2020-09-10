# Forecasting News Topic popularity using Neural Topic Model and Amazon Forecast

In these notebooks, we will explore how to incorporate unstructured text data into time-series forecasting problems. While traditional
time series approaches typically rely on univariate numerical data, algorithms such as DeepAR+ recipe (https://docs.aws.amazon.com/forecast/latest/dg/aws-forecast-recipe-deeparplus.html)
in Amazon Forecast allow users to bring other numerical and categorical information as related-time series data. 

However some data formats, particularly unstructured data such as text, while can influence future valuese of a time series, cannot be directly included 
in these algorithms. Example use cases where this might apply is forecasting product sales in stores or e-commerce based on customer reviews, forecasting the popularity of articles or blogs
based on user reviews, forecasting values of financial instruments based on news topics and headlines besides simply from a sentiment score etc. 

## Requirements:

1/ Since text pre-processing can be memory intensive, it is recommended that you use a **ml.t3.xlarge** (or equivalent) instance to run your notebook. This will prevent any out-of-memory errors.

2/ Make sure that you are using a region where Amazon Forecast is currently available. The most recent list can be found here: https://aws.amazon.com/about-aws/whats-new/2020/03/amazon-forecast-is-now-available-in-three-new-regions-asia-pacific-sydney-mumbai-and-europe-frankfurt/

3/ Amazon SageMaker will need an IAM role to use Amazon Forecast. Once you clone this repo in your SageMaker Notebook environment, go to IAM and add the AmazonForecastFullAccess policy to your SageMaker Notebook IAM role.

4/ You will also need to ensure that Amazon Forecast can access the S3 bucket containing your data. While this is not a recommended best practice, for this demo, you can create a role in IAM with Amazon Forecast as the Service Principal that allows Access to Amazon S3.
More details on how to do this can be found here: https://docs.aws.amazon.com/forecast/latest/dg/getting-started.html

**Note**: the permissive IAM policies suggested above are for demo purposes only, for production environments you want to restrict access based on least privelege principles.


In this set of 3 notebooks we will complete the following steps:

1. **1_preprocess.ipynb**: Download and pre-process a dataset to predict news popularity based on headlines and news sentiment.

2. **2_NTM.ipynb**
  
  a. Rather than treatng this as a regression problem, we will illustrate a different approach where we view each Topic as a time series.
  
  b. We then extract the news headlines using text pre-processing and train a Neural Topic Model (https://docs.aws.amazon.com/sagemaker/latest/dg/ntm.html)
  to extract topic vectors
   
  c. This notebook shows how to pre-process the text dataset to make it usable as a time-series.
  
  
3. **3_Forecast.ipynb**

  a. We use the topic vectors generated in 2_NTM notebook as related time series to predict the popularity of topics using the  DeepAR+ algorithm ong Amazon Forecast, a fully managed service for
  creating a time series forecast. We will access and call Amazon Forecast APIs using a Jupyter notebook on Amazon SageMaker. Once we train a recipe and create a predictor, we will visualize the predicted forecast in the notebook.

 
  
  

