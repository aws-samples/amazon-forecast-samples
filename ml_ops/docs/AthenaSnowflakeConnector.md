## Connecting Snowflake to Amazon Forecast through Amazon Athena Federated Query

This is an optional process that can extend the Amazon Forecast MLOps base deployment by allowing customers to retrieve historical data from their Snowflake environment and prepare it for ingestion into Amazon Forecast.

## Installing the CloudFormation Stack
This procedure will create a new VPC with both private and public subnets and a NAT gateway that allows connectivity to Snowflake.  This stack also installs a Lambda function that helps facilitate a JDBC connection to Snowflake and securely stores your username and password using AWS Secrets Manager.  Effectively, this process is the bridge that connects Amazon Athena to Snowflake.

1. From the AWS Console, navigate to the CloudFormation service.  Next, click "Create Stack" and select "with new resources (Standard)" option.

3. At stack creation, "Step 1: Specify template" paste the Amazon S3 URL string into the control as follows:
	 ```
   https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/athena-snowflake-connector.yaml
   ```
4. Click Next to continue.

5. At stack creation, "Step 2: Specify stack details", several parameters are collected that define how the entire workload behaves.  You can edit these according to each use case.  You might also elect to save a template with your own desired default values.  

The following table helps define each parameter.

| Parameter | Description |
|--|--|
| Stack name |  Provide the stack name such as snowflake-amazon-connector |
|AthenaDataSourceName|This defines the name of the Athena Data source and will be used in your SQL statement.|
|LambdaFunctionName|This will establish the name of your Lambda Function.   Name this accordingly if you have many Snowflake sources to consider.|
|S3Bucket|The S3 bucket where Amazon Athena will write intermediate results|
|SecretsManagerName|They key name used to store the username and password in AWS Secrets Manager |
|SnowflakeAccount|Your Snowflake account name excluding a the snowflakecomputing.com portion. |
|SnowflakeDatabase|Your Snowflake database name|
|SnowflakeSchema|The default schema used|
|SnowflakeUsername|Snowflake username string|
|SnowflakePassword|Snowflake password string|
|SnowflakeWarehouse|Name of the warehouse|

5. Click next.
6. At stack creation, "Step 3: Configure stack options", go to the bottom of the page and click next.
7. At stack creation, "Step 4: Review", there is check are several check boxes to acknowledge resources are being created.  Check them only after reviewing them, then click next.
8. The installation process takes between 5-10 minutes to complete.

## Setting up your SQL to pull data from Snowflake

In this section, you will need to define the queries you wish to submit to Snowflake.  These effectively qualify and shape data records according to your business need.  Amazon Forecast supports three distinct kinds of data inputs as [defined here](https://github.com/aws-samples/amazon-forecast-samples/blob/main/library/content/Datasets.md).   After understanding the intention of Target Time Series (TTS), Related TIme Series (RTS) and Item Metadata you can start start to write SQL statements with proper WHERE, GROUP BY, SELECT and joint clauses to get the right data desired, in the right shape.  The resulting queries will end on Amazon S3 as CSV files which Amazon Forecast can easily import.

We recommend you write the queries and test them out first in your Snowflake console or BI tool.  Once you've perfected them, you will store the SQL statement inside AWS Systems Manager Parameter Store.   Prior to storing these in Parameter Store, test your Athena Connection.

## Testing Connection in Amazon Athena

1. Navigate to Amazon Athena in your AWS console and ensure you are in the same region as you had installed your Amazon Forecast MLOps stack and Snowflake connector stack.
2. In the Athena editor, select the dropdown for Data source.  You should choose <b>snowflake_forecast_connector</b>, or the alternate value you chose during the CloudFormation deployment.
3. Select the correct database at dropdown.
4. You can paste your SQL in the left query pane and click run to test it out.  
5. If this works, you have demonstrated each of your queries are valid syntax and they move to Amazon correctly.  This also validates your password and network connection was successful.

## Installing SQL into Amazon Forecast MLOps

1. Navigate to Systems Manager in your console by typing SSM in the search control at the top.
2. Once at Systems Manager, select <b>Parameter Store</b> in the left pane.
3. A list of parameters will appear.  You can add a filter in the search control as follows:
```
/forecast/{your-stack-name}/DatasetGroup/Query
```
4. The filter in the last step will return three keys for RTS, TTS and Item Metadata.  Open each of these that apply for you, by clicking on the item name and selecting <b>Edit</b>.
5. Once in edit mode, paste the SQL inside the <b>value</b> control and click <b>Save Changes</b>.
6. Repeat this for each SQL you are submitting.  TTS is mandatory, the others are optional.
7. Remove the filter for parameters by clicking on the X and set a new filter as follows
```
/forecast/{your-stack-name}/DatasetGroup/DatasetInclude
```
8. If you are submitting RTS, change the value to true.
9. If you are submitting Item Metadata, change the value to true.


## Running your Athena-Connector Step Function

1. Navigate to Step Functions in your console and click on <b>State Machines</b>.
2. In the search control, type the name of your base Solution Guidance stack.  You will see several State Machines including one named as <b>{stack-name}-Athena-Connector</b>.  Click on this to open it.
3. Click Start Execution, then Start Execution a second time to launch without any changing any input parameters.
4. You can observe the state machine running.  The idea is it runs each of your queries, returning data to Amazon S3, where the next Amazon MLOps Step function will import the data for model training or inference.



## Important Considerations
-  As delivered, there is a default limit of 500,000 rows retrieved per SQL query.  We have load tested this several million rows of data, but you will need to change settings in the Lambda function to enable more than 500,000.  Open the Lambda function you created as part of the CloudFormation deployment.  By default, the name was <b>snowflake_forecast_connector</b>.   Click on the Configuration tab choose the <b>Environment Variables</b> item from the left pane.  Change the pagecount value from 500000 to as appropriate for your workload.

- If you have any memory errors with Lambda from large datasets, you can increase the memory from 3008MB as delivered to as high as 10240MB.  Open the Lambda function you created as part of the CloudFormation deployment.  By default, the name was <b>snowflake_forecast_connector</b>.   Click on the Configuration tab choose the <b>Edit</b> on the right side of the page.  Change the memory setting as appropriate for your workload to a max of 10240MB.


If you have any questions, please contact your AWS Solution Architect and ask for assistance.
