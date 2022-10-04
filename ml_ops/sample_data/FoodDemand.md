## Food Demand Use Case

This example is based a synthetic dataset of food products by location.  In this scenario, the company must anticipate how many of each item, at each location will be demanded, so they can have enough to cover on-shelf demand.  As a synthetic dataset, the purpose of this data isn't to produce highly accurate insights; instead this is to demonstrate a workflow pattern so you can understand how to adapt your own data for use with Amazon Forecast.

Instead of following the [normal set of steps provided for the MLOps workflow](https://github.com/aws-samples/amazon-forecast-samples/tree/main/ml_ops), you may use this dataset as an override.

1. Complete the [MLOps dependency stack](https://github.com/aws-samples/amazon-forecast-samples/blob/main/ml_ops/docs/DependencyStack.md) prior to attemping the instructions below.  The MLOps dependency stack creates necessary underlying permissions.  This step only needs to occur once per AWS account.
2.  Once the MLOPs dependency stack is in place, navigate to [CloudFormation service](https://us-west-2.console.aws.amazon.com/cloudformation) and select your desired deployment region.
3.  Click the "Create Stack, with new resources (Standard)".
4.  Provide "fooddemo" as Stack Name and provide the following URL as the Amazon S3 URL.  You may [download the file](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/forecast-mlops-solution-guidance.yaml) locally or clone using git.

	 ```
     https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/forecast-mlops-solution-guidance.yaml
     ```

5.  "Step 2: Specify stack details", several parameters are collected that define how the entire workload behaves.  Use these overrides.

| Parameter | Recommended Value |
|--|--|
|Stack name|fooddemo|
|DatasetGroupFrequencyRTS|W|
|DatasetGroupFrequencyTTS|W|
|DatasetGroupName|fooddemo|
|DatasetIncludeItem|true|
|DatasetIncludeRTS|true|
|ForecastForecastTypes|["0.50"]|
|PredictorExplainPredictor| TRUE
|PredictorForecastDimensions |["location_id"]|
|PredictorForecastFrequency |W|
|PredictorForecastHorizon | 10|
|PredictorForecastOptimizationMetric| AverageWeightedQuantileLoss|
|PredictorForecastTypes | ["0.30", "0.40", "0.50", "0.60", "0.70"]|
|S3Bucket | {your bucket} |
|SNSEndpoint | {your email} |
|TimestampFormatRTS |yyyy-MM-dd|
|TimestampFormatTTS |yyyy-MM-dd|

These next set of values are multi-line and can be copied to your clipboard with the copy icon and pasted into the CloudFormation parameter.

<b>PredictorAttributeConfigs</b>
```
[
    {
      "AttributeName": "checkout_price",
      "Transformations": {
        "backfill": "mean",
        "futurefill": "mean",
        "middlefill": "mean"
      }
    },
    {
      "AttributeName": "base_price",
      "Transformations": {
        "backfill": "mean",
        "futurefill": "mean",
        "middlefill": "mean"
      }
    },
    {
      "AttributeName": "emailer_for_promotion",
      "Transformations": {
        "backfill": "zero",
        "futurefill": "zero",
        "middlefill": "zero"
      }
    },
    {
      "AttributeName": "homepage_featured",
      "Transformations": {
        "backfill": "zero",
        "futurefill": "zero",
        "middlefill": "zero"
      }
    },
    {
      "AttributeName": "target_value",
      "Transformations": {
        "aggregation": "sum",
        "backfill": "nan",
        "frontfill": "none",
        "middlefill": "nan"
      }
    }
]
```   

<b>SchemaITEM</b>
```
{
    "Attributes": [
    {
      "AttributeName": "item_id",
      "AttributeType": "string"
    },
    {
      "AttributeName": "food_category",
      "AttributeType": "string"
    },
    {
      "AttributeName": "food_cuisine",
      "AttributeType": "string"
    }
    ]
}
```   

<b>SchemaRTS</b>
```
{
    "Attributes": [
    {
      "AttributeName": "location_id",
      "AttributeType": "string"
    },
    {
      "AttributeName": "item_id",
      "AttributeType": "string"
    },
    {
      "AttributeName": "checkout_price",
      "AttributeType": "float"
    },
    {
      "AttributeName": "base_price",
      "AttributeType": "float"
    },
    {
      "AttributeName": "emailer_for_promotion",
      "AttributeType": "integer"
    },
    {
      "AttributeName": "homepage_featured",
      "AttributeType": "integer"
    },
    {
      "AttributeName": "timestamp",
      "AttributeType": "timestamp"
    }
    ]
}
```   

<b>SchemaTTS</b>
```
{
    "Attributes": [
    {
      "AttributeName": "location_id",
      "AttributeType": "string"
    },
    {
      "AttributeName": "item_id",
      "AttributeType": "string"
    },
    {
      "AttributeName": "target_value",
      "AttributeType": "integer"
    },
    {
      "AttributeName": "timestamp",
      "AttributeType": "timestamp"
    }
    ]
}
```   
6. Download a unique dataset: [FoodDemand.zip](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/FoodDemand.zip)
7. Unzip this file on your laptop and then upload the uncompressed folders and files to your S3 bucket, inside a child <b>retaildemo</b> folder.  Please note the S3 bucket and child stack folder that will contain the tts and rts folder should match the Stack Name and S3 bucket name from above.  Stated differently, if your Stack Name is abc123, the top-level folder in your S3 bucket should also be named abc123.
8. Resume the overall instruction set for MLOps [here](https://github.com/aws-samples/amazon-forecast-samples/blob/main/ml_ops/docs/UploadData.md).  This page directs you to download [FoodDemand.zip](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/FoodDemand.zip), uncompress it and then upload to S3.

## Conclusion

The steps above help you understand how produce a forecast on a synthetic dataset.  Please use overrides as a way to learn how to adapt data to your bespoke schema and use case.  If you have any questions, please reach out to your AWS Solutions Architect or account team.
