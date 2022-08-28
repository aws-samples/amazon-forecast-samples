## Retail Forecasting Use Case

This example is based on a public dataset available through [Kaggle](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting) which contains real-world weekly sales data provided by a major retailer.  Departmental level sales data was made available for a small sample of stores for partial periods in years 2010-2012.

Instead of following the normal set of steps provided for the MLOps workflow, you may use this dataset as an override.

1.  Navigate to [CloudFormation service](https://us-west-2.console.aws.amazon.com/cloudformation) and select your correct region.  Selecting the correct region is important.
2.  Click the "Create Stack, with new resources (Standard)".
3.  Provide "retaildemo" as Stack Name and provide the following URL as the Amazon S3 URL.
 
	 ```
     https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/forecast-mlops-solution-guidance.yaml
     ```
	If needed, you may [download the file](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/forecast-mlops-solution-guidance.yaml) locally or clone using git.

4.  "Step 2: Specify stack details", several parameters are collected that define how the entire workload behaves.  Use these overrides.

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
5. You will need to download the prepared dataset: [RetailData.zip](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/RetailData.zip)
6. Unzip this file on your laptop and then upload the folders and files to your S3 bucket, inside a child <b>retaildemo</b> folder.  Please note the S3 bucket and child folder that will contain the tts and rts folder should match the Stack Name and S3 bucket name from above.   Stated differently, if your Stack Name is abc123, the top-level folder in your S3 bucket should also be named abc123.

## Conclusion

The steps above help you understand how to override the default MLOps toy dataset with an alternate Kaggle originated set.  Please use these overrides as a way to learn how to adapt data to your bespoke schema and use case.  If you have any questions, please reach out to your AWS Solutions Architect or account team.
