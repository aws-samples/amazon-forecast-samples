# Amazon Forecast pre-POC Workshop - hands-on Bring Your own Data

In this workshop, you will get hands-on and learn how to use Amazon Forecast with your own data.  We will go through a complete data pipeline.  From raw data input - to training a model on that data - to generating inferences (forecasts) from the model - to exporting and visualizing the forecasts.  

This workshop is designed to accelerate customers doing an Amazon Forecast POC.  The architecture components will make experimentation and iteration of Forecast models easier for your POC project.  The components installed during the workshop can remain in your account after the workshop, so you can keep using these tools to perform experimentation with Forecast models.

By default, the installed AWS service components do not incur any cost when not in use.  

- [ ] Warning:  SageMaker is the only AWS service in this solution you need to take extra precautions about when not in use.  As installed, the Forecast solution will not incur cost.  However, if you do open a SageMaker Notebook, make sure to shut down all Notebook instances when not in use, otherwise SageMaker will keep charging, even when not in use.

##### Audience

Developers and/or Data Scientists who will be doing the POC work.

##### Cost

Assume 10 students each training their own models all day, with big data $15GB, each student generating 300K forecasts (10*300K forecasts).  Expected cost $31 Forecast + $23 QuickSight + $50 SageMaker + $1 S3 + $1 Glue + $0.20 Athena + free tier Lambda, Step Functions, SNS (make sure everyone shuts down their Notebook instances end of day otherwise cost could be a lot more) = $106.20.  

Budget $200 total for the workshop should cover everything.



### AWS Trainer - Get Ready for the Workshop

**1 month before the workshop**

Ask customer to create an AWS sandbox account for running the POC.  Data migration from on-premise might need to be set up.  Customer should put their POC data into an S3 bucket in this AWS sandbox account.  

- Confirm what data customer will use.  
- Confirm with customer that it is acceptable for AWS staff to temporarily access the sandbox account for purpose of conducting the Pre-POC workshop training.  We won't set up the access yet.

**2 weeks before the workshop** 

Customer to send AWS staff leading the workshop an anonymized sample of data.  

- AWS staff customize the Data Prep template notebooks to the customer's data. 
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

**3 days before the workshop** - AWS staff needs access to customer's account

Install the Amazon Forecast solution CloudFormation template in the customer's sandbox account they plan to use for the POC.  Total install time ~15min.  

- Log into customer's account with Admin account 
- [Follow these instructionse:  install-forecast-solution.md](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/install-forecast-solution.md)
- Sign up for QuickSight Enterprise, get the ARN
  - Update CloudFormation nested (main) stack with QuickSight ARN
- Make a note and verify S3 bucket where customer's POC data is located.
- Send customer your finished .ipynb Data Prep template customized to their data
- Identify the SageMaker notebook instance configured with solution
  - Edit github repo:  https://github.com/aws-samples/amazon-forecast-samples
  - Inspect notebook instance IAM policy
    - Make sure it can access S3 and run Forecast
  - Verify notebook instance starts up and you can see the 2 workshop notebooks 
  - Upload your customized notebook to the notebook instance
  - Make sure your notebook runs completely start-to-finish before the day of training.
  - Important!!  Stop the SageMaker notebook instance.





### Day of workshop.  Typical agenda.

| **Start** | **End** | Who                      | **Activity**                                                 |
| --------- | ------- | ------------------------ | ------------------------------------------------------------ |
| 9:00a     | 9:30a   | Customer                 | Introductions, customer's Exec sponsor set the stage of the exact problem that is to be tackled and what success looks like for the POC engagement. |
| 9:30a     | 10:00a  | AWS                      | Slides - High-level overview of Amazon Forecast              |
| 10:00a    | 10:30a  | AWS                      | Demo - Console demo of NYC taxi data. <br /> (Show the DataPrep notebook, Forecast console, DataSet, Predictor, Forecast, Exports, QuickSight Dashboard) |
| 10:30a    | 10:45a  | All                      | Discussion - mapping customer's data to the Forecast POC problem<br />AWS Trainer TODO just before break: <br />- start up SageMaker notebook instance <br/>- Choose compute ml.t3.2xlarge, see https://aws.amazon.com/sagemaker/pricing/ <br/>- Choose EBS permanent storage 5GB default<br />- Show where the code Repo is specified (github or AWS CodeBuild). |
| 10:45     | 11:00   | BREAK                    | 15min BREAK                                                  |
| 11:00a    | 12:00p  | AWS leading the customer | Prepare data - we'll use the template DataPrep notebook <br />- Ask customer to upload the .ipynb you already prepared to the running Notebook instance<br />- Get the S3 location where customer keeps their data<br />- Customize S3 location where notebook data will be saved<br />- You can run pretty quickly through the Notebook<br />- Verify S3 location where notebook data was saved<br />Launch Predictor using just TTS and AutoML using the solution<br />- Edit the .yaml file<br />- Find the training S3 bucket<br />- upload .yaml file in root of S3 bucket; copy customer's S3 data in train/ folder |
| 12:00p    | 1:00p   | LUNCH                    | 1hr LUNCH<br />AWS Trainer TODO just before lunch break: <br />- check that the predictor launched<br />- check step functions make sure no errors |
| 1:00p     | 1:30p   | AWS                      | Overview Solution Architecture components                    |
| 1:30p     | 2pm     | AWS leading customer     | Evaluate Predictor (in console, using Query, and in QuickSight) |
| 2:00p     | 2:30p   | AWS leading customer     | Start Discussion:  Iterate on Dataset and Models <br /<br />- Show customer github link CheatSheet<br />- Show the NYC taxi Quicksight Model Comparison Dashboard |
| 2:30p     | 2:45p   | AWS                      | Summarize what was learned                                   |
| 2:45p     | 3:15p   | Customer                 | Presentation to Exec Sponsor what they learned, accomplished, and possible next steps |
| 3:15p     | 3:30p   | AWS                      | Answer Questions<br />Ask customer to leave you a Review<br /> |
| 4:00p End |         | AWS + Customer           | - Remove AWS staff temporary access to the POC sandbox account<br />- IMPORTANT - STOP ALL SAGEMAKER NOTEBOOK INSTANCES BEFORE LEAVING FOR THE DAY!! |