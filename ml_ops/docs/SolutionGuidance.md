## Deploying workload-specific Amazon Forecast Solution Guidance

You may repeat this process as a quick start for each use case you intend to deploy.  Each use case is separated by virtue of being an independent CloudFormation stack.

1. In the AWS console, select the desired region for workload deployment.  The Amazon Forecast service is available in these [AWS Regions](https://docs.aws.amazon.com/general/latest/gr/forecast.html).  The region selector can be found, as a dropdown, right-of-center on the black menu bar in the AWS Console.  Choose the option that best meets your needs, but do take care to choose a region where AWS Forecast is available.
2. From the AWS Console, navigate to the CloudFormation service.  You can do this by tying CloudFormation in the "search for services" control in the black menu bar.  Next, click the orange "Create Stack" button.  If using the drop down, select "with new resources (Standard)" option.

3. At stack creation, "[Step 1: Specify template](../images/create-solution-guidance-stack-1.jpg)", simply paste the URL string into the control as follows:

	 ```
     https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/forecast-mlops-solution-guidance.yaml
     ```

	If needed, you may [download the file](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/forecast-mlops-solution-guidance.yaml) locally or clone using git.
4. Click Next to continue.

5. At stack creation, "Step 2: Specify stack details", several parameters are collected that define how the entire workload behaves.  You can edit these according to each use case.  You might also elect to save a template with your own desired default values.  

As delivered, there is a demo set of data.  For learning, you may accept all these fields as-is, but you will need to provide a S3Bucket and SNSEndpoint value -- these are the only two blank items below.  If you are learning, you can skip to step 6; however, if you are configuring this for your use case, pay particular attention to each.  Many of these fields are editable later, to change how your workload behaves at runtime.

The following table helps define each parameter.

| Parameter | Description | More Information |
|--|--|--|
| Stack name |  Provide the stack name as a short name that represents the use case.  This must be unique, please take care not to include characters other than A through Z and numbers 0 through 9.  Example stack names are:  workload1, RegionXYZWeeklyDemand. |
|DatasetGroupFrequencyRTS|The frequency of data collection for RELATED TIME SERIES dataset|select from dropdown|
|DatasetGroupFrequencyTTS|The frequency of data collection for TARGET TIME SERIES dataset|select from dropdown|
|DatasetGroupName|Short name for dataset group, a self-contained workload.|[CreateDatasetGroup](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateDatasetGroup.md)|
|DatasetIncludeItem|Do you wish to provide item metadata for this use-case?|select from dropdown
|DatasetIncludeRTS|Do you wish to provide a related time series (RTS) for this use-case?|select from dropdown
| ForecastForecastTypes| When a CreateForecast job runs, this declares which quantiles to produce predictions for.  You may choose up to 5 values in this array.  Edit this value to include values according to need.| [CreateForecast](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateForecast.md)
|PredictorAttributeConfigs | For the target variable in Target Time Series each numeric field in the Related Time Series datasets, a record must be created for each time-interval for each item.  This configuration helps determine how missing records are filled in, with zeros, will NaN or otherwise. We recommend that you fill the gaps in the target time series with NaN instead of 0. Filling with 0, the model might learn wrongly to bias forecasts toward 0. NaN is how the guidance is delivered.  Consult with your AWS Solution Architect with any questions on this. | [CreateAutoPredictor](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateAutoPredictor.md)
|PredictorExplainPredictor| Valid values are TRUE or FALSE. These determine if Explainability is enabled for your predictor.  This can help you understand how values in the RTS and Item Metadata influence the model. | [Explainability](https://docs.aws.amazon.com/forecast/latest/dg/forecast-explainability.html)
|PredictorForecastDimensions |You may want to forecast at a finer grain than item.  Here, you can specify dimensions such as location, cost center or whatever your needs are.  This needs to agree with the dimensions in your RTS and TTS.  Important note:  if you have no dimension, the correct parameter is the word null.  Null should be by itself and in all lower case.  Null is a reserved word that lets the system know there is no parameter for dimension.| [CreateAutoPredictor](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateAutoPredictor.md)
|PredictorForecastFrequency |Defines the time scale at which your model and predictions will be generated, such as daily, weekly, or monthly. The dropdown selector helps you choose allowed values.  This will need to agree with your RTS time scale if you are using RTS. | [CreateAutoPredictor](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateAutoPredictor.md)
|PredictorForecastHorizon | The number of time-steps that the model predicts. The forecast horizon is also called the prediction length. | [CreateAutoPredictor](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateAutoPredictor.md)
|PredictorForecastOptimizationMetric|Defines the accuracy metric used to optimize the predictor. The dropdown will help you select, Weighted Quantile Loss balances over/under forecasting.  RMSE is concerned with units and WAPE/MAPE are concerned with percent errors. | [CreateAutoPredictor](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateAutoPredictor.md)
|PredictorForecastTypes | When a CreateAutoPredictor job runs, this declares which quantiles are used to train prediction points.  You may choose up to 5 values in this array, allowing you to balance over-and-under forecasting.  Edit this value to include values according to need.| [Link](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateAutoPredictor.md)
|S3Bucket | The name of the S3 bucket where input data and output data are written for this workload. |
|SNSEndpoint | A valid e-mail address to receive notifications when Predictor and Forecast jobs are complete. |
|SchemaITEM| This defines the physical order, column names, and data types for your Item Metadata dataset.  This is an optional file provided in the Solution Guidance example. | [CreateDataset](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateDataset.md)
|SchemaRTS |This defines the physical order, column names and data types for your Related Time Series dataset. The dimensions must agree with your Target Time Series.  The time-grain of this file governs the time-grain at which  predictions can be made.  This is an optional file provided in the Solution Guidance example. |[CreateDataset](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateDataset.md)
|SchemaTTS| This defines the physical order, column names, and data types for your Target Time Series dataset, the only required dataset.  The file must contain a target value, timestamp, and item at a minimum. |[CreateDataset](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateDataset.md)
|TimestampFormatRTS | Defines the timestamp format provided in the RTS file. | [CreateDatasetImportJob](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateDatasetImportJob.md)
|TimestampFormatTTS | Defines the timestamp format provided in the TTS file. |[CreateDatasetImportJob](https://github.com/awsdocs/amazon-forecast-developer-guide/blob/main/doc_source/API_CreateDatasetImportJob.md)|

<br> Be sure to ask your AWS Solutions Architect for clarity, when in doubt.

6. At stack creation, "Step 3: Configure stack options", go to the bottom of the page and click next.
7. At stack creation, "Step 4: Review", there is no check the box with this iteration because there are no IAM resources created.   Click next.

## Confirm E-mail Subscription

1. Shortly (within ~15 minutes) after the stack is deployed, you will receive an e-mail.

2. Open the email and click "confirm subscription".

When the CloudFormation Stack completes, your workload-specific deployment is complete.<br><br>
NEXT: Now you can shift to operating the workflow! Click to start here with [uploading data to S3](UploadData.md).
