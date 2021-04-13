# Amazon Forecast Samples

Notebooks and examples on how to onboard and use various features of Amazon Forecast

## Getting Started Notebooks

This is a place where you will find various examples covering Amazon Forecast best practices

Open the [notebooks](notebooks/) folder to find a CloudFormation template that will deploy all the resources you need to build your first campaign with Amazon Personalize. The notebooks provided can also serve as a template to building your own models with your own data.

In the [*notebooks*](notebooks/) folder you will learn to:

1. Prepare a dataset for use with Amazon Forecast.
2. Build models based on that dataset.
3. Evaluate a model's performance based on real observations.
4. How to evaluate the value of a Forecast compared to another.

## MLOps with AWS Step Functions

This is a place where you will find various examples covering Machine Learning Operations best practices.

To get started navigate to the [ml_ops](ml_ops/) folder and follow the README instructions.

In the [*ml_ops*](ml_ops) folder you will learn how to:

1. Deploy an automated end to end pipeline from training to visualization of your Amazon Forecasts in Amazon QuickSight

## No code workshop

In this repository, you will find a tutorial to walk you through an energy consumption use case with two different methods:

1. For the first method, you will only use the service console and this will be 100% no-code: use this [markdown file](workshops/no_code_workshop/forecast-with-console.md) to follow along.
2. For the second method, you will fire up a SageMaker Notebook Instance and perform exactly the same process by using the Amazon Forecast API as documented [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecast.html) (for datasets and models management features) and [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/forecastquery.html) (for the query service): run [this notebook](no_code_workshop/forecast-with-api.ipynb) to dive deeper in these APIs.


## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
