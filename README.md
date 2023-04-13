# Amazon Forecast Samples

Workshops, Notebooks and examples on how to learn and use various features of Amazon Forecast


##  Announcements and New Service Features 

 - [Learn in a workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/b28f3502-ca9f-4e12-8b84-59e454c1ed53/en-US)
 - [Building a Strong Time-Series ML Model: AutoPredictor](./library/content/AutoPredictor.md)
 - [New Feature: Forecast with Cold-Start Items](./notebooks/advanced/Forecast%20with%20Cold%20Start%20Items/Forecast%20with%20Cold%20Start%20Items.ipynb)
 - [New Feature: What-if Analysis](./notebooks/advanced/WhatIf_Analysis/WhatIf_Analysis.ipynb)
 - [New Feature: Custom Time Alignment Boundary](./notebooks/advanced/Custom_Time_Alignment_Boundary/Time_Alignment_Boundary_Introduction.ipynb)
 - [New Feature: Forecast on Selected Time-Series](./notebooks/advanced/Forecast_Selected_TimeSeries/Forecast_Selected_TimeSeries_Introduction.ipynb)
 - [New Feature: Predictor Monitoring](./notebooks/advanced/Predictor_Monitoring/Predictor_Monitoring_Introduction.ipynb)
 - [No Code Guide to Automate Forecast for PoC and production workloads](./ml_ops/README.md)
 - [Python developers: A Quick Start Guide](./notebooks/basic/Getting_Started/Amazon_Forecast_Quick_Start_Guide.ipynb)
 

##  Introduction and Best Practices

Please [visit our growing library](./library/README.md) which serves as a guide for onboarding data and learning how to use Amazon Forecast.


## MLOps: Run a proof of concept (PoC) and learn how to automate production workloads

![MLOps Automation](./ml_ops/images/forecast-cycle.jpg)<br>

The purpose of this guidance is to provide customers with a complete end-to-end workflow that serves as an example -- a model to follow.  As delivered, the guidance creates forecasted data points from an open-source input data set.  The template can be used to create Amazon Forecast Dataset Groups, import data, train machine learning models, and produce forecasted data points, on future unseen time horizons from raw data.  All of this is possible without having to write or compile code.  [Get Started Here](./ml_ops/README.md)

## Notebooks

Here you will find examples how to use Amazon Forecast Python SDK to make API calls, with manual waits between API calls.  Primary audience is Developers, MLOps Enginners, and Integration Partners who need to see how to put forecasts into production.

- Getting started notebooks:
  - [Get Started with Amazon Forecast](./notebooks/basic/Getting_Started/Amazon_Forecast_Quick_Start_Guide.ipynb) 
  - [Upgrading to AutoPredictor](./notebooks/basic/Upgrading_to_AutoPredictor/UpgradeToAutoPredictor.ipynb)

- Advanced folder contains notebooks to show API calls for more complex tasks:
  - [Time Series Clustering Preprocessing](./notebooks/advanced/Clustering_Preprocessing/README.md)
  - [Using the Amazon Forecast Weather Index](./notebooks/advanced/Weather_index/1.%20Training%20your%20model%20with%20Weather%20Index.ipynb)
  - [Incorporating Related data](./notebooks/advanced/Incorporating_Related_Time_Series_dataset_to_your_Predictor/Incorporating%20Related%20Time%20Series%20dataset%20to%20your%20Predictor.ipynb) 
  - [Incorporating Item Meta data](./notebooks/advanced/Incorporating_Item_Metadata_Dataset_to_your_Predictor/Incorporating_Item_Metadata_Dataset_to_your_Predictor.ipynb) 
  - [Assessing item level accuracy using custom metrics with Predictor backtest exported data](./notebooks/advanced/Item_Level_Accuracy/Item_Level_Accuracy_Using_Bike_Example.ipynb) 


## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
