# Instructions how to install the Amazon Forecast solution

The Amazon Forecast Pre-POC workshop uses a solution that is implemented using AWS service components bundled together and deployed using AWS CloudFormation template.  The architecture components will make experimentation and iteration of Forecast models easier.

By default, the installed components of this solution do not incur any cost when not in use. 

- [ ] Warning:  SageMaker is the only AWS service in this solution you need to take extra precautions about when not in use.  As installed, it will not incur cost.  However, if you do open a SageMaker Notebook, make sure to shut down all Notebook instances when not in use, otherwise SageMaker will keep charging, even when not in use.

## Details

The CloudFormation template used in this workshop will:

* Deploy the Improving <a href="https://docs.aws.amazon.com/solutions/latest/improving-forecast-accuracy-with-machine-learning/automated-deployment.html" target="_blank">Forecast Accuracy with Machine Learning</a> solution main AWS CloudFormation (nested) template.
* Deploy the NYC taxi demo data (target time series, related time series, item metadata) into the solution Amazon S3 Bucket.  
* Automatically launch a demo NYC taxi forecast in Amazon Forecast.

Below is an architecture diagram of components used in this solution.

![cloudformationautomation-architecture](https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/cloudformationautomation-architecture.png)

## Prerequisites

Before starting the workshop, make sure you have logged into your AWS account and installed our CloudFormation template:

1. **Log in to your AWS account**. If you do not already have one, <a href="https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/" target="_blank">create an AWS account</a>.
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

Performing the above steps will deploy a demonstration stack using data from the <a href="https://registry.opendata.aws/nyc-tlc-trip-records-pds/" target="_blank">NYC Taxi Dataset</a>.

## Deploying a CloudFormation template for Amazon Forecast Automation

Follow the steps below to deploy the CloudFormation template using the NYC Taxi Dataset.

**Step 1**: Accept defaults, click "Next"

<img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/cloudformationautomation-step1.png" alt="cloudformationautomation-step1" style="zoom:80%;" />



**Step 2:** Name your stack "forecast-stack-nyctaxi-demo" and provide an email address for notifications. Click "Next".

<img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/cloudformationautomation-step2.png" alt="cloudformationautomation-step2" style="zoom:80%;" />

**Step 3**: Accept defaults, click "Next"

**Step 4:** Click both checkboxes to allow IAM resources to be created and to allow possibly nested stacks. Click “Create Stack”

<img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/cloudformationautomation-step4.png" style="zoom:80%;">

**Step 5:** Open your email and confirm subscription to notifications.

<img src="https://amazon-forecast-samples.s3-us-west-2.amazonaws.com/common/images/workshops/cloudformationautomation-step5.png" style="zoom:80%;">

<br>
That’s it! You have deployed a CloudFormation template in Amazon Forecast. <br>

**Cleaning Up:** Deleting the demo stack will retain the "Improving Forecast Accuracy with Machine Learning Stack". Deleting the "Improving Forecast Accuracy with Machine Learning" stack will leave all S3, Athena, QuickSight, and Forecast data in the customer account.

**Other deployment options**: For more deployment options, see <a href="https://docs.aws.amazon.com/solutions/latest/improving-forecast-accuracy-with-machine-learning/automated-deployment.html" target="_blank">Automated Deployment</a>.  If data is already available, you can deploy the stack without the demo data.

