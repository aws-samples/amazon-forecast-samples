# Amazon Forecast pre-POC Workshop - hands-on Bring Your own Data

In this workshop, you will get hands-on and learn how to use Amazon Forecast with your own data.  We will go through a complete data pipeline.  From raw data input - to training a model on that data - to generating inferences (forecasts) from the model - to exporting and visualizing the forecasts.  

![](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/forecast_overview.png)

This workshop is designed to accelerate customers doing an Amazon Forecast POC.  The architecture components will make experimentation and iteration of Forecast models easier for your POC project.  The components installed during the workshop can remain in your account after the workshop, so you can keep using these tools to perform experimentation with Forecast models. <br>


### 3 days before workshop, install the demo (an AWS CloudFormation template)  
Install the [Improving Forecast Accuracy With Machine Learning Solution](https://aws.amazon.com/solutions/implementations/improving-forecast-accuracy-with-machine-learning/) AWS CloudFormation template in your AWS account where you will run the Forecast POC.  This best practice AWS solution streamlines the process of ingesting, modeling, and forecasting using Amazon Forecast by providing AWS CloudFormation templates and a workflow around the Amazon Forecast service.<br>

Total install time ~15min.

1. Log in to AWS with Admin account:  [console.aws.amazon.com](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/console.aws.amazon.com)
2. [Follow these instructions](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/install-forecast-solution.md)
3. Read the [Blog using this Solution for Electric Load Forecasting](https://aws.amazon.com/blogs/industries/short-term-electric-load-forecasting-with-amazon-forecast/)

By default, the installed AWS service components do not incur any cost when not in use.  

- [ ] Warning:  SageMaker is the only AWS service in this solution you need to take extra precautions about when not in use.  As installed, the Forecast solution will not incur cost.  However, if you do open a SageMaker Notebook, make sure to shut down all Notebook instances when not in use, otherwise SageMaker will keep charging, even when not in use.



### Day of workshop.  Typical agenda.

- | **Start** | **End** | Who          | **Activity**                                                 |
  | --------- | ------- | ------------ | ------------------------------------------------------------ |
  | 9:00a     | 9:30a   | Customer     | Introductions, customer's Exec sponsor set the stage of the exact problem that is to be tackled and what success looks like for the POC engagement. |
  | 9:30a     | 9:45a   | AWS          | High-level overview of Amazon Forecast<br />[See Amazon Forecast Introduction](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#intro) |
  | 9:45      | 10:00a  | AWS          | [Demo video: watch minutes 8-18](https://www.youtube.com/watch?v=K7MaDbn8_l0) |
  | 10:00a    | 10:15a  | AWS          | Theory - mapping customer's data to the Forecast POC problem. [See Mapping your data into time series](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#mapping)<br />Theory - data preparation, why it's needed, what it is.  [See Data Prep Best Practices](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#dataprep) |
  | 10:15     | 11:00   | Lab          | Hands-on Lab - Prepare your data <br/><br />**Developers:**  Suggest using [AWS Glue DataBrew](https://aws.amazon.com/glue/features/databrew/), a data preparation UI tool, to clean data and save TTS to S3.  TODO link 5min video<br />**Data Scientists:**  We have DataPrep Jupyter notebook templates.  We have included data prep steps we have noticed are common in customers' data.<br />- If data is Hourly or below - [use the regular DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb) and save TTS to S3<br /> - If data is Daily or Weekly - [use the weekly DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi_weekly.ipynb) and save TTS to S3 |
  | 11:00     | 11:15   | BREAK        | 15min BREAK                                                  |
  | 11:15     | 11:45   | AWS          | Theory - Best practices for getting the most accuracy from your data <br />Reading: [See Amazon Forecast Best Practices, Steps 1-10](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice)<br />Video: [watch this 10min video, minutes 21-31](https://www.youtube.com/watch?v=K7MaDbn8_l0). |
  | 11:45a    | 12:00p  | Lab          | Hands-on Lab - Train your first Predictor using just TTS and AutoML<br />1. Download [taxi demo data TTS csv](https://amazon-forecast-samples.s3.amazonaws.com/automation_solution/demo-nyctaxi/nyctaxi_weather_auto.csv)<br />2. Upload TTS csv file to S3, copy S3 URI save somewhere locally.<br />**Option#1:  Launch using the solution**:<br />3. [Copy/paste/edit locally the .yaml file](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/forecast-defaults.yaml)<br />4. Upload .yaml file to root of solution S3 bucket <br />5. Find the train/ folder of solution S3 bucket<br />6. Copy the S3 URI of TTS data to root of solution's S3 train/ folder<br /><br />**Option#2: Launch using console**:  [See Getting Started Tutorial, Steps 11-18](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#tutorial). |
  | 12:00p    | 1:00p   | LUNCH        | 1hr LUNCH<br />                                              |
  | 1:00p     | 1:30p   | AWS          | [Overview Improving Forecast Accuracy with ML Solution Architecture components](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/install-forecast-solution.md) |
  | 1:30p     | 1:45p   | BREAK        | 15min BREAK                                                  |
  | 1:30p     | 1:45p   | Lab          | Hands-on: Evaluate Predictor (in console, and in QuickSight)<br />[See Getting Started Tutorial, Steps 19-21](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#tutorial) |
  | 1:45p     | 2:00p   | Lab          | Hands-on: Create Forecast (in console, in Query, and in QuickSight)<br />[See Generating Forecasts](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#forecastinference) |
  | 2:00p     | 2:30p   | AWS          | Theory -  Iterating on Dataset and Models and scaling to value<br />[See Iterating Models / What-if Best Practices, Steps 23-29](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#iteratebp)<br /> |
  | 2:30p     | 2:45p   | AWS          | Summarize what was learned                                   |
  | 2:45p     | 3:15p   | Customer     | Presentation to Exec Sponsor what they learned, accomplished, and possible next steps |
  | 3:15p     | 3:30p   | END WORKSHOP | [Additional Resources](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#notebooks) |

