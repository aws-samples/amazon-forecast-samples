# Instructions how to install the Amazon Forecast solution

The Amazon Forecast Pre-POC workshop uses a solution that is implemented using AWS service components bundled together and deployed using AWS CloudFormation template.  The architecture components will make experimentation and iteration of Forecast models easier.

By default, the installed components of this solution do not incur any cost when not in use. 

- [ ] Warning:  SageMaker is the only AWS service in this solution you need to take extra precautions about when not in use.  As installed, it will not incur cost.  However, if you do open a SageMaker Notebook, make sure to shut down all Notebook instances when not in use, otherwise SageMaker will keep charging, even when not in use.

## Details

The CloudFormation template used in this workshop will:

* Deploy the Improving <a href="https://docs.aws.amazon.com/solutions/latest/improving-forecast-accuracy-with-machine-learning/automated-deployment.html" target="_blank">Forecast Accuracy with Machine Learning</a> solution main AWS CloudFormation (nested) template.
* Deploy the NYC taxi demo data (target time series, related time series, item metadata) into the solution Amazon S3 Bucket.  
* Automatically launch a demo NYC taxi forecast in Amazon Forecast.

Below is an architecture diagram of components used in this solution, showing how it is used in Development Mode.

![cloudformationautomation-architecture](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/architectureDevMode.png)

Also showing how the architecture is used in Production Mode. 

![cloudformationautomation-architecture](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/architectureProdMode.png)

## Instructions

Before starting the workshop, log into your AWS account and install our CloudFormation template:

1. **Log in to AWS using an Admin account**. If you do not already have one, <a href="https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/" target="_blank">create an AWS account</a>.
2. **Install the AWS CloudFormation template.** Choose the Region closest to you:

   * Tokyo: <a href="https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank"> ap-northeast-1</a>
   * Seoul: <a href="https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank">ap-northeast-2</a>
   * Mumbai: <a href="https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank">ap-south-1</a>
   * Singapore: <a href="https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank">ap-southeast-1</a>
   * Sydney: <a href="https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank">ap-southeast-2</a>
   * Frankfurt: <a href="https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank">eu-cental-1</a>
   * Ireland: <a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank">eu-west-1</a>
   * N. Virginia: <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank">us-east-1</a>
   * Ohio: <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank">us-east-2</a>
   * Oregon: <a href="https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template" target="_blank">us-west-2</a>

## Next, follow these directions for the screens that will pop up:

**Step 1**: Accept defaults, click "Next"

<img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/cloudformationautomation-step1.png" style="zoom:60%;" />



**Step 2:** Name your stack "forecast-stack-nyctaxi-demo" and provide an email address for notifications. Click "Next".

<img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/cloudformationautomation-step2.png" style="zoom:60%;" />

**Step 3**: Accept defaults, click "Next"

**Step 4:** Click both checkboxes to allow IAM resources to be created and to allow possibly nested stacks. Click “Create Stack”

<img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/cloudformationautomation-step4.png" style="zoom:60%;">

**Step 5:** Open your email and confirm subscription to notifications.

<img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/cloudformationautomation-step5.png" style="zoom:60%;">

That’s it! You have deployed a CloudFormation template in Amazon Forecast. 

Performing the above steps deployed a demonstration stack called "forecast-stack" using data from the <a href="https://registry.opendata.aws/nyc-tlc-trip-records-pds/" target="_blank">NYC Taxi Dataset</a>.  The main stack called "forecast-stack-ForecastStack-xxxx" will be a nested stack. <br><br>

**Optional steps for QuickSight visualization:**
1. Sign up for [QuickSight Enterprise](https://aws.amazon.com/quicksight/pricing/).  Per user cost is $5/month which should be enough if everyone is logging in using "Admin" account.
2. Click on "Admin" in top-right corner of QuickSight.  Get your QuickSight ARN.  Note "ARN" means Amazon Resource Number, think of it as an AWS-specialized URL.   Construct ARN following this pattern: <br> 
"arn:aws:quicksight:<region>:<account ID>::user/default/<Username>" <br>
 Example: arn:aws:quicksight:us-east-1:12345678901:user/default/Admin/myusername
3. Copy QuickSight ARN somewhere locally, and copy to your clipboard. <br>
<br>
Next, we need to configure where QuickSight is allowed to read data.
4. Quicksight > top right Admin > Change region > US-east-1 N.VA. Due to a quirk in QuickSight, configuration tasks only work in us-east-1.
5. Quicksight > top right Admin > Manage Quicksight 
6. Quicksight > left-side-menu > Security & permissions > Main screen > Access to AWS Services > click “Add or Remove” button
[TODO image here]
<br>
Configure permission to read from S3 buckets<br>
7. Click S3 Details
8. Click forecast-stack-athenabucket-xxx + click RHS “write” checkbox
9. Click forecast-stack-data-bucket-xxx + click RHS “write” checkbox + click Finish
10. Click S3 RHS checkbox (If you do not have any S3 buckets, you will be prompted to create a S3 bucket before you can enable it)
11. Click Finish
[TODO image here]
<br>
Configure permission to read from Athena<br>
12. Click Athena RHS checkbox
13. Scroll to bottom of screen > click “Update” box
[TODO image here]
<br>
Now edit the CloudFormation nested (main) stack called "forecast-stack-xxxx" and add your QuickSight ARN <br>
14. Click button next to the nested stack and click menu action “Update”
[TODO image here]
<br>
15. Click "Update nested stack"
[TODO image here]
16. Choose “Use current template” > “Next”
[TODO image here]
17. Edit fields.  
    1. Change “Email” if it's not already set.
    2. Change “Visualization Options” > paste your QuickSight arn <br>

<br>

**Cleaning Up:** Deleting the demo stack will retain the "Improving Forecast Accuracy with Machine Learning Stack". Deleting the "Improving Forecast Accuracy with Machine Learning" stack will leave all S3, Athena, QuickSight, and Forecast data in the customer account.

**Other deployment options**: For more deployment options, see <a href="https://docs.aws.amazon.com/solutions/latest/improving-forecast-accuracy-with-machine-learning/automated-deployment.html" target="_blank">Automated Deployment</a>.  If data is already available, you can deploy the stack without the demo data.

