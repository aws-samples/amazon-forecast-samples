# Amazon Forecast Automation Workshop

In this workshop, you will get hands-on training how to use Amazon Forecast. The Automation stack will automatically launch a forecast pipeline using NYC taxi demo data. But then, we would like you to think how to use your own data to create forecasts.

The Amazon Forecast CloudFormation stack used in this workshop will:

* Deploy the "[Improving Forecast Accuracy with Machine Learning](https://docs.aws.amazon.com/solutions/latest/improving-forecast-accuracy-with-machine-learning/automated-deployment.html)" solution AWS CloudFormation template.
* Deploy the NYC taxi demo (target time series, related time series, item metadata) to the solution Forecast Data Amazon S3 Bucket.
* Automatically trigger the demo NYC taxi forecast pipeline in Amazon Forecast.

Below is an architecture diagram of components used in this workshop.
[Image: images/cloudformationautomation-architecture.png]

### Prerequisites

Before starting the workshop, make sure you have logged into your AWS account and installed our CloudFormation template:

1. **Log in to your AWS account**. If you do not already have one, [create an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).
2. **Install the AWS CloudFormation template.** Choose the Region closest to you:

   * Tokyo: [ap-northeast-1](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)
   * Seoul: [ap-northeast-2](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)
   * Mumbai: [ap-south-1](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)
   * Singapore: [ap-southeast-1](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)
   * Sydney: [ap-southeast-2](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)
   * Frankfurt: [eu-cental-1](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)
   * Ireland: [eu-west-1](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)
   * N. Virginia: [us-east-1](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)
   * Ohio: [us-east-2](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)
   * Oregon: [us-west-2](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=forecast-stack&templateURL=https:%2F%2Fs3.amazonaws.com%2Fsolutions-reference%2Fimproving-forecast-accuracy-with-machine-learning%2Flatest%2Fimproving-forecast-accuracy-with-machine-learning-demo.template)

Performing the above steps will deploy a demonstration stack using our [NYC Taxi Dataset](https://registry.opendata.aws/nyc-tlc-trip-records-pds/).

## Deploying a CloudFormation template for Amazon Forecast Automation

Follow the steps below to deploy the CloudFormation template using the NYC Taxi Dataset.

**Step 1**: Accept defaults, click "Next"
[Image: images/cloudformationautomation-step1.png]
**Step 2:** Name your stack "forecast-stack-nyctaxi-demo" and provide an email address for notifications. Click "Next".
[Image: images/cloudformationautomation-step2.png]
**Step 3**: Accept defaults, click "Next"

**Step 4:** Step 4: Click both checkboxes to allow IAM resources to be created and to allow possibly nested stacks. Click “Create Stack”
[Image: images/cloudformationautomation-step4.png]

That’s it! You have deployed a CloudFormation template in Amazon Forecast.

**Cleaning Up:** Deleting the demo stack will retain the "Improving Forecast Accuracy with Machine Learning Stack". Deleting the "Improving Forecast Accuracy with Machine Learning" stack will leave all S3, Athena, QuickSight, and Forecast data in the customer account.

**Other deployment options**: For more deployment options, see [Automated Deployment](https://docs.aws.amazon.com/solutions/latest/improving-forecast-accuracy-with-machine-learning/automated-deployment.html).  If data is already available, you can deploy the stack without the demo data.
