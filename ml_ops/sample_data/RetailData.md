## Retail Forecasting Use Case

This example is inspired by a public dataset available through [Kaggle](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting) which contains real-world weekly sales data provided by a major retailer.  Departmental level sales data was made available for a small sample of stores for partial periods in years 2010-2012.  The Kaggle competition concluded years ago; the purpose of this page is not to compete but to demonstrate how to forecast a public set of data with Amazon Forecast.  More importantly, this allows you to understand how to adapt your own data for use with Amazon Forecast.

This dataset is available at other repositories:
- (Github)[https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-on-Amazon-Web-Services/tree/master/Chapter11/deep-ar/data]
- (Kaggle)[https://www.kaggle.com/datasets/manjeetsingh/retaildataset]


Instead of following the [normal set of steps provided for the MLOps workflow](https://github.com/aws-samples/amazon-forecast-samples/tree/main/ml_ops), you may use this dataset as an override.

1. Complete the [MLOps dependency stack](https://github.com/aws-samples/amazon-forecast-samples/blob/main/ml_ops/docs/DependencyStack.md) prior to attemping the instructions below.  The MLOps dependency stack creates necessary underlying permissions.  This step only needs to occur once per AWS account.
2.  Once the MLOPs dependency stack is in place, navigate to [CloudFormation service](https://us-west-2.console.aws.amazon.com/cloudformation) and select your desired deployment region.
3.  Click the "Create Stack, with new resources (Standard)".
4.  Provide "retaildemo" as Stack Name and provide the following URL as the Amazon S3 URL.  You may [download the file](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/forecast-mlops-solution-guidance.yaml) locally or clone using git.

	 ```
     https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/forecast-mlops-solution-guidance.yaml
     ```

5.  "Step 2: Specify stack details", several parameters are collected that define how the entire workload behaves.  Use these overrides.

| Parameter | Recommended Value |
|--|--|
|Stack name|retaildemo|
|DatasetGroupFrequencyRTS|W|
|DatasetGroupFrequencyTTS|W|
|DatasetGroupName|retaildemo|
|DatasetIncludeItem|false|
|DatasetIncludeRTS|true|
|ForecastForecastTypes|["0.50"]|
|PredictorExplainPredictor| TRUE
|PredictorForecastDimensions |["dept"]|
|PredictorForecastFrequency |W|
|PredictorForecastHorizon | 12|
|PredictorForecastOptimizationMetric| AverageWeightedQuantileLoss|
|PredictorForecastTypes | ["0.30", "0.40", "0.50", "0.60", "0.70"]|
|S3Bucket | {your bucket} |
|SNSEndpoint | {your email} |
|SchemaITEM| null |
|TimestampFormatRTS |yyyy-MM-dd|
|TimestampFormatTTS |yyyy-MM-dd|

These next set of values are multi-line and can be copied to your clipboard with the copy icon and pasted into the CloudFormation parameter.

<b>PredictorAttributeConfigs</b>
```
[
   {
      "AttributeName":"target_value",
      "Transformations":{
         "aggregation":"sum",
         "backfill":"nan",
         "frontfill":"none",
         "middlefill":"nan"
      }
   }
]
```   


<b>SchemaRTS</b>
```
{
   "Attributes":[
      {
         "AttributeName":"item_id",
         "AttributeType":"string"
      },
      {
         "AttributeName":"timestamp",
         "AttributeType":"timestamp"
      },
      {
         "AttributeName":"dept",
         "AttributeType":"string"
      },
      {
         "AttributeName":"temperature",
         "AttributeType":"float"
      },
      {
         "AttributeName":"fuel",
         "AttributeType":"float"
      },
      {
         "AttributeName":"markdown1",
         "AttributeType":"float"
      },
      {
         "AttributeName":"markdown2",
         "AttributeType":"float"
      },
      {
         "AttributeName":"markdown3",
         "AttributeType":"float"
      },
      {
         "AttributeName":"markdown4",
         "AttributeType":"float"
      },
      {
         "AttributeName":"markdown5",
         "AttributeType":"float"
      },
      {
         "AttributeName":"cpi",
         "AttributeType":"float"
      },
      {
         "AttributeName":"unemployment",
         "AttributeType":"float"
      },
      {
         "AttributeName":"holiday",
         "AttributeType":"float"
      }
   ]
}
```   

<b>SchemaTTS</b>
```
{
   "Attributes":[
      {
         "AttributeName":"item_id",
         "AttributeType":"string"
      },
      {
         "AttributeName":"timestamp",
         "AttributeType":"timestamp"
      },
      {
         "AttributeName":"dept",
         "AttributeType":"string"
      },
      {
         "AttributeName":"target_value",
         "AttributeType":"float"
      }
   ]
}
```   
6. Download the prepared dataset, which is inspired by the original: [RetailData.zip](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/RetailData.zip)
7. Unzip this file on your laptop and then upload the uncompressed folders and files to your S3 bucket, inside a child <b>retaildemo</b> folder.  Please note the S3 bucket and child stack folder that will contain the tts and rts folder should match the Stack Name and S3 bucket name from above.  Stated differently, if your Stack Name is abc123, the top-level folder in your S3 bucket should also be named abc123.
8. Resume the overall instruction set for MLOps [here](https://github.com/aws-samples/amazon-forecast-samples/blob/main/ml_ops/docs/UploadData.md).  However; on the next page, instead of using the sample dataset as directed, use the [RetailData.zip](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/RetailData.zip) file obtained on this page as an override.

## Conclusion

The steps above help you understand how to override the default MLOps toy dataset with an alternate Kaggle originated set.  Please use these overrides as a way to learn how to adapt data to your bespoke schema and use case.  If you have any questions, please reach out to your AWS Solutions Architect or account team.
