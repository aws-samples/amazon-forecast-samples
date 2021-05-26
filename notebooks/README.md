# Notebooks

Here you will find examples how to use Amazon Forecast Python SDK to make API calls, with manual waits between API calls.  Primary audience is Developers, MLOps Enginners, and Integration Partners who need to see how to put forecasts into production.

For detailed specifics of any concept mentioned look at the [Forecast developer guide](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html) and this github [Introduction, Best Practices Tutorial](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md).

- Basic folder contains introductory notebooks to show API calls to:
  - [import data containing 1 single item](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/basic/Tutorial/1.Importing_Your_Data.ipynb)
  - [train a predictor and forecast on a single item](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/basic/Tutorial/2.Building_Your_Predictor.ipynb)
  - [query and evaluate one item at a time](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/basic/Tutorial/3.Evaluating_Your_Predictor.ipynb)
  
- Advanced folder contains notebooks to show API calls for more complex tasks:
  - [Using the Amazon Forecast Weather Index](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Weather_index/1.%20Training%20your%20model%20with%20Weather%20Index.ipynb)
  - [Incorporating Related data](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Incorporating_Related_Time_Series_dataset_to_your_Predictor/Incorporating_Related_Time_Series_dataset_to_your_Predictor.ipynb) 
  - [Incorporating Item Meta data](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Incorporating_Item_Metadata_Dataset_to_your_Predictor/Incorporating_Item_Metadata_Dataset_to_your_Predictor.ipynb) 
  - [Assessing item level accuracy using custom metrics with Predictor backtest exported data](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Item_Level_Accuracy/Item_Level_Accuracy_Using_Bike_Example.ipynb) 
  - [Forecasting "cold-start" or new product introductions by generating test data explicitly filled with "NaN" for new items and running Forecast-only (that is inference only) using already trained predictor](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Forecast%20with%20Cold%20Start%20Items/Forecast%20with%20Cold%20Start%20Items.ipynb) 


<br>

## FAQ

**Q. How do I contribute my own example notebook?**

A. Although we're extremely excited to receive contributions from the community, we're still working on the best mechanism to take in examples from external sources. Please bear with us in the short-term if pull requests take longer than expected or are closed.

<br>

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.

