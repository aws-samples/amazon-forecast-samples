
# Mapping your data into Amazon Forecast datasets


## Dataset group<a name="datasetgroup"/>
A  _dataset group_ is a collection of one to three complimentary datasets, one of each dataset type.  You import datasets to a dataset group, then use the dataset group to train a predictor and generate forecasts.  Ultimately, the dataset group is a self-contained unit that holds all related Amazon Forecast artifacts for a single workload including data, ML model and inference.  Customers may create many dataset groups, one for each workload, where a shared-nothing design is needed. 
<br>There are three customer supplied dataset types: 

 - [Target Time Series](./TargetTimeSeries.md), required dataset
 - [Related Time Series](./RelatedTimeSeries.md), optional
 - [Item Metadata](./ItemMetadata.md), optional

<br>
In addition, AWS curates and provides these datasets for forecasts that can benefit from sensitivity to holidays and weather: 
 
 - [Weather Index](./WeatherIndex.md), AWS supplied dataset
 - [Holidays Featurization](./HolidaysFeaturization.md), AWS supplied dataset


<br><br>
[Return to Table of Contents](../README.md)
