# Amazon Forecast pre-POC Workshop - hands-on Bring Your own Data

In this workshop, you will get hands-on and learn how to use Amazon Forecast with your own data.  We will go through a complete data pipeline.  From raw data input - to training a model on that data - to generating inferences (forecasts) from the model - to exporting and visualizing the forecasts.  

![](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/forecast_overview_steps.png)

This workshop is designed to accelerate customers doing an Amazon Forecast POC.  The architecture components will make experimentation and iteration of Forecast models easier for your POC project.  The components installed during the workshop can remain in your account after the workshop, so you can keep using these tools to perform experimentation with Forecast models. <br>



##### Audience

Developers and/or Data Scientists who will be doing the POC work.

##### Cost

Assume 10 students each training their own models all day, with big data $15GB, each student generating 300K forecasts (10*300K forecasts).  Expected cost $31 Forecast + $23 QuickSight + $50 SageMaker + $1 S3 + $1 Glue + $0.20 Athena + free tier Lambda, Step Functions, SNS (make sure everyone shuts down their Notebook instances end of day otherwise cost could be a lot more) = $106.20.  

Budget $200 total for the workshop should cover everything.



### Three ways to use this workshop

1. **Self-service training.**  You can bring your own data, and follow along all the steps below, starting with "Install the demo".  You'll need time to customize the [Data Prep notebook to your data](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb).  Best Practice theory is mixed-in along with Hands-on Lab instructions.  
2. **AWS- or AWS Partner-led training as a no-code, no-hands-on, canned demo**.  [See the separate instructions](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/AWS_instructions.md) and look for notes about "canned demo".  Follow the below instructions to "Install the demo" before day of your demo.  The NYC Taxi demo will be created for you automatically.  All you have to do is open AWS console to Amazon Forecast, and walk audience through the completed screens in the Forecast Dataset Group called "nyctaxi_weather_auto".
3. **AWS- or AWS Partner-led hands-on, bring your own data, pre-POC workshop.**  [See the separate instructions](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/AWS_instructions.md).  For best results, ask for a sample of customer's anonymized POC data at least 1 week in advance.  You'll need time to customize the [Data Prep notebook to their data](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb).  You'll also need follow the below instructions to "Install the demo" beforehand.  Day of the workshop, share the customized Data Prep notebook with customer, so they can more quickly get going with their Forecast POC.



### AWS (or Partner) Trainer - Get Ready for the Workshop

**1 month before the workshop**

Ask customer to create an AWS sandbox account for running the POC.  Data migration from on-premise might need to be set up.  Customer should put their POC data into an S3 bucket in this AWS sandbox account.  

- Confirm what data customer will use.  
- Confirm with customer that it is acceptable for Instructor staff to temporarily access the sandbox account for purpose of conducting the Pre-POC workshop training.  We won't set up the access yet.

**2 weeks before the workshop** 

Customer to send Instructor staff leading the workshop an anonymized sample of data.  

- Instructor customize the Data Prep template notebooks to the customer's data. 

  - If data is daily or finer-grained - [use the regular DataPrep template notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi_template.ipynb)
  - If data is weekly or bigger-grained - [use the weekly DataPrep template notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi_weekly_template.ipynb)

- Confirm POC Forecast choices:  

  - Forecast time unit granularity?  
    - Choices are Y|M|W|D|H|30min|15min|10min|5min|1min
  - How many time units (forecast length)?  
    - For example, if your time unit is H, then if you want to forecast out 1 week, that would be 24*7 = 168 hours, so forecast length = 168.  
    - Rule: Forecast length cannot be longer than 1/3 of training data.
  - Data time granularity? 
    - Usually the same as forecast granularity
    - Rule: Data granularity can be <= forecast time unit granularity.

- **3 days before the workshop** - Instructor needs access to customer's account to follow instructions below "Install the demo".

  


### Install the demo (an AWS CloudFormation template)  
Three days before the workshop, install the [Improving Forecast Accuracy With Machine Learning Solution](https://aws.amazon.com/solutions/implementations/improving-forecast-accuracy-with-machine-learning/) AWS CloudFormation template in your AWS account where you will run the Forecast POC.  This best practice AWS solution streamlines the workflow around Amazon Forecast of ingesting, modeling, forecasting, and visualizing with Amazon QuickSight through an AWS CloudFormation template.

The template will make experimentation and iteration of Forecast models easier.  

Total install time ~15min.

1. Log into customer's account with Admin account 
2. [Follow these instructions](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/install-forecast-solution.md)
3. Make a note and verify S3 bucket where customer's POC data is located.
4. Send customer your finished .ipynb Data Prep template customized to their data
5. Identify the SageMaker notebook instance configured with solution
   - Edit github repo:  https://github.com/aws-samples/amazon-forecast-samples
   - Inspect notebook instance IAM policy
     - Make sure it can access S3 and run Forecast
   - Verify notebook instance starts up and you can see the 2 workshop notebooks 
   - Upload your customized notebook to the notebook instance
   - Make sure your notebook runs completely start-to-finish before the day of training.
6. Important!!  Stop the SageMaker notebook instance.

By default, the installed AWS service components do not incur any cost when not in use.  

- [ ] Warning:  SageMaker is the only AWS service in this solution you need to take extra precautions about when not in use.  As installed, the Forecast solution will not incur cost.  However, if you do open a SageMaker Notebook, make sure to shut down all Notebook instances when not in use, otherwise SageMaker will keep charging, even when not in use.



### Day of workshop.  Typical agenda.

- | **Start** | **End** | **Activity**                                                 |
  | --------- | ------- | ------------------------------------------------------------ |
  | 9:00a     | 9:30a   | Introductions, customer's Exec sponsor set the stage of the exact problem that is to be tackled and what success looks like for the POC engagement. |
  | 9:30a     | 9:45a   | High-level overview of Amazon Forecast<br />[See Amazon Forecast Introduction](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#intro) |
  | 9:45      | 10:00a  | [Demo video: watch minutes 8-18](https://www.youtube.com/watch?v=K7MaDbn8_l0) |
  | 10:00a    | 10:15a  | 1. Theory - mapping customer's data to the Forecast POC problem. [See Mapping your data into time series](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#mapping)<br />2. Theory - data preparation, why it's needed, what it is.  [See Data Prep Best Practices](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#dataprep) |
  | 10:15     | 11:00   | HANDS-ON LAB - PREPARE YOUR DATA <br/><br />**Instructor:  To run this lab as a canned demo:**<br />Skip this lab since demo data already prepared.<br /><br />**BI Analysts or Developers:**  Suggest using [AWS Glue DataBrew](https://aws.amazon.com/glue/features/databrew/), a data preparation UI tool, to clean data and save TTS to S3.  TODO link 5min video<br /><br />**Data Scientists:**  See the DataPrep Jupyter notebook which includes common data prep steps.<br />- If data is Hourly or below - [use the regular DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb) and save TTS and optionally RTS, IM to S3<br /> - If data is Daily or Weekly - [use the weekly DataPrep notebook](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi_weekly.ipynb) and save TTS to S3<br />1. Open aws console.  console.amazon.com > open Sagemaker  <br />2. On left menu open Notebook > Notebook instances.  Main screen orange button "Create notebook instance"<br />3. - Choose compute ml.t3.2xlarge, see https://aws.amazon.com/sagemaker/pricing/ <br/>- Choose EBS permanent storage 5GB default<br />- Find where the code Repo is specified (github or AWS CodeBuild).<br />- In the github config part, type https://github.com/aws-samples<br />- Scroll to bottom, click "Update notebook instance"<br />- Start your notebook<br />4. Open regular Jupyter notebook (not JupyterLab) <br />5. Navigate to the notebook you're using today under "workshops/pre_POC_workshop/"<br />6. Choose kernel conda_python3 > Set Kernel<br />7. File > make a copy - so you keep original to see what run cells should look like<br />8. Kernel > Restart and Clear Output<br />9. Edit notebook,  look for hints # EDIT THIS FOR YOUR DATA<br />See if you can follow along using your own data |
  | 11:00     | 11:15   | 15min BREAK                                                  |
  | 11:15     | 11:45   | 1. Theory - Best practices for getting the most accuracy from your data. [See Amazon Forecast Best Practices, Steps 1-10](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#bestpractice)<br />2. Video: [watch this 10min video, minutes 21-31](https://www.youtube.com/watch?v=K7MaDbn8_l0). |
  | 11:45a    | 12:00p  | HANDS-ON LAB - IMPORT DATA AND TRAIN YOUR FIRST PREDICTOR<br />**Instructor:  To run this lab as a canned demo:**<br />1. Download [taxi demo data TTS csv](https://amazon-forecast-samples.s3.amazonaws.com/automation_solution/demo-nyctaxi/nyctaxi_weather_auto.csv)<br />2. Upload `nyctaxi_weather_auto.csv` file to your S3 bucket<br />3. After you see "Upload succeeded", click orange "Close" button.  Use S3 Action "Query with S3 Select" to show what the data looks like.  <br />4. Download also [RTS  csv](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/automation_solution/demo-nyctaxi/nyctaxi_weather_auto.related.csv) and [IM csv](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/automation_solution/demo-nyctaxi/nyctaxi_weather_auto.metadata.csv) files. <br />6. Repeat steps 2-3 above for the  RTS and IM files<br />7. Open Forecast console.<br />8. Show the console steps that are already running automatically for you under dataset group "nyctaxi_weather_auto".<br />9. Optional - [Download the file "forecast-defaults.yaml"](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/forecast-defaults.yaml) to show how the automation was configured. <br />10. If you're running a canned demo, students don't do any Hands-on Labs.<br /><br />**Student Instructions:**<br />1. [Open aws console](), log in, and navigate to S3.   <br />2. **Find where you saved** your Target Time Series **in your S3 bucket**.<br />3. **Click blue link to your TTS csv file**.  Look for button on top right, **click "Copy S3 URI"**.  Save S3 URI somewhere convenient.<br /><br />**Option#1:  Launch using the automation solution**:<br />Follow steps below.  Also here is a demo video. <br />4. If using additional data, find where you saved IM and RTS files in your S3 bucket. Click blue link to each file, click "Copy S3 URI", save each S3 URI somewhere convenient.  <br />5. **Open a new AWS console browser tab, navigate to S3**. <br />6. **Click on the solution S3 bucket** to view it.   Hint:  type ""forecast-stack-data-bucket"" in S3 search.  You should see bucket called ""forecast-stack-data-bucket-xxxx"" and the Region where you downloaded the solution.<br />7. **Find the file `forecast-defaults.yaml` and Download it**  (click little box to left, then click menu button "Download").<br />8. If using your own data, edit your local copy of `forecast-defaults.yaml`.   [See documentation](https://docs.aws.amazon.com/solutions/latest/improving-forecast-accuracy-with-machine-learning/overriding-forecast-defaults.html).<br />9. If you changed it, upload edited `forecast-defaults.yaml` file back to root of solution S3 bucket you found in Step 5  (click orange "Upload" button). <br />10. **Click train/ folder** in solution S3 bucket and **copy the S3 URI of the train folder**.  <ctrl-c> or <command-c> to Save S3 URI in your clipboard.  <br />11. **Go back to other S3 browser tab, for your own S3 bucket**, from Step 2.  Locate your training files(s).  **Check the little boxes to left of your files, choose Actions, choose Copy**.  <br />12. **In the "Destination" space, paste the S3 URI from step 9 for the solution train/ folder**.  Scroll down, verify the files names are correct, then **click orange button "Copy"**.<br />That's it!  If you follow the above Lab Steps, the next 2 labs will be completed automatically for you.<br /><br />**Option#2: Launch using console**:  <br />1. [Watch demo video how to import data using screens](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/demo_videos/video_import_console.mp4) (6min)<br />2. [See Getting Started Tutorial, Steps 11-14](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#tutorial).  <br />3. Watch [demo video](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/demo_videos/video_train_eval_console.mp4) how to train a predictor using screen (minutes 1-2:30)<br />4. [See Getting Started Tutorial, Steps 15-18.](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#tutorial)<br />Unlike the automatic Option#1, you will need to wait between the Data Import step and the Train Predictor steps.  Also, you will need to do the next 2 Labs also in console.<br /><br />**Both Option#1 and Option#2.**  Before going to lunch, **verify your Predictor is training**: <br />1. Open AWS console.  **Open Amazon Forecast service.**<br />2. **Click "View dataset groups "**<br />3. **Click "nytaxi_weather_auto"** on the top of the list.  <br />4. **Verify Datasets** have been **imported**<br />5. **Verify Predictor is training** <br />6. Option#1 only.  Open another console tab.  Search for "step functions".  Open Step Functions.  Look for State Machine called "Improving-Forecast-Accuracy-forecast-stack-ForecastStack-xxxx".  Click it. Under "Executions" look for a running execution.  Click it.  What you should see is all the steps that have run already (highlighted in green), and all the steps that are running (blue). |
  | 12:00p    | 1:00p   | 1hr LUNCH<br />**Instructor: Make sure your demo Predictor is running before leaving for lunch.**  <br />- Check Forecast console<br />- Check Step Functions, make sure you don't see errors. |
  | 1:00p     | 1:30p   | Theory - [Overview Improving Forecast Accuracy with ML Solution Architecture components](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/install-forecast-solution.md) |
  | 1:30p     | 1:45p   | 15min BREAK                                                  |
  | 1:30p     | 1:45p   | HANDS-ON LAB - EVALUATE PREDICTOR<br />1. [Watch demo video](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/demo_videos/video_train_eval_console.mp4) how to evaluate a predictor (minutes 2:30-6) <br />2. [See Getting Started Tutorial, Steps 19-21](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#tutorial) |
  | 1:45p     | 2:00p   | HANDS-ON LAB - CREATE A FORECAST, EXPORT FORECAST, QUERY FORECAST, VISUALIZE PREDICTORS AND FORECASTS IN QUICKSIGHT DASHBOARD<br />1. [Watch a demo video](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/demo_videos/video_create_query_vis_forecast.mp4) (2min)<br />2. [See Generating Forecasts](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#forecastinference) |
  | 2:00p     | 2:30p   | Theory -  Iterating on Dataset and Models and scaling to value<br />[See Iterating Models / What-if Best Practices, Steps 23-29](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#iteratebp) |
  | 2:30p     | 2:45p   | Summarize what was learned                                   |
  | 2:45p     | 3:15p   | Presentation to Exec Sponsor what they learned, accomplished, and possible next steps |
  | 3:15      | 3:30p   | IMPORTANT!! IF YOU OPENED ANY SAGEMAKER NOTEBOOK INSTANCES, SHUT THEM DOWN BEFORE LEAVING END OF DAY!!  Otherwise SageMaker will keep charging, even when not in use.<br />**Instructor:**  Remove AWS staff temporary access to the POC sandbox account. |
  | 3:15p     | 3:30p   | [Additional Resources](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md#notebooks) |
  | 3:30p     | 3:30p   | END OF WORKSHOP                                              |

