## Amazon Forecast Samples

This goal of this repository is to provide a common starting point for learning how to use the various features of [Amazon Forecast](https://aws.amazon.com/forecast/). 

For detailed specifics of any concept mentioned look at the [Forecast developer guide](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html)

In the Notebooks you will learn to:

1. Prepare a dataset for use with Amazon Forecast.
1. Build models based on that dataset.
1. Evaluate a model's performance based on real observations.
1. How to evaluate the value of a Forecast compared to another.

## Agenda

The steps below outline the process of building your own time-series prediction models, evaluating them, and then cleaning up all of yuour resources to prevent any unwanted charges. To get started execute the following steps.

1. Deploy the CloudFormation Template below or build a local Jupyter environment with the AWS CLI installed and configured for your IAM account.
1. [Getting_Data_Ready.ipynb](basic/Tutorial/1.Getting_Data_Ready.ipynb) - Guides you through preparing your dataset to be used with Amazon Forecast.
1. [Building_Your_Predictor.ipynb](basic/Tutorial/2.Building_Your_Predictor.ipynb) - Explains how to use the dataset you prepared to build your first model.
1. [Evaluating_Your_Predictor.ipynb](basic/Tutorial/3.Evaluating_Your_Predictor.ipynb) - Takes the model you just created and evaluates its performance against real observed measurements.
1. [Cleanup.ipynb](basic/Tutorial/4.Cleanup.ipynb) - Deletes Amazon Forecast resources and IAM role created in above notebooks.

Each notebook can be found within the `notebooks` folder in this project.

## Prerequisites 

1. An AWS Account
1. A user in the account with administrative privileges


## Outline

1. First you will deploy a CloudFormation template that will create an S3 bucket for data storage, a SageMaker Notebook Instance where the exercises are executed, IAM policies for the Notebook Instance, and it will clone this repository into the Notebook Instance so you are ready to get started.
1. Next you will open the `Getting_Data_Ready.ipynb` to get started.
1. This notebook will guide you through the process of the other notebooks until you have a working and evaluated forecast.


## Building Your Environment:

As mentioned above, the first step is to deploy a CloudFormation template that will perform much of the initial setup work for you. In another browser window or tab, login to your AWS account. Once you have done that, open the link below in a new tab to start the process of deploying the items you need via CloudFormation.

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=ForecastDemo&templateURL=https://chriskingpartnershare.s3.amazonaws.com/ForecastDemo.yaml)

Follow along with the screenshots below if you have any questions about deploying the stack.

### Cloud Formation Wizard

Start by clicking `Next` at the bottom like this:

![StackWizard](doc/images/img1.png)

If you choose to provide a S3 bucket name for your file storage in the next page, remember that bucket names must be globally unique: If you enter a bucket name that already exists in any AWS account, your stack will fail to create.

You can instead leave this option blank to create a bucket name automatically, and leave other options as default unless you need to change them. Once you're ready, click Next again.

![StackWizard2](doc/images/img2.png)

This page is a bit longer so scroll to the bottom to click `Next`.

![StackWizard3](doc/images/img4.png)


Again scroll to the bottom, check the box to enable the template to create new IAM resources and then click `Create Stack`.

![StackWizard4](doc/images/img5.png)

For a few minutes CloudFormation will be creating the resources described above on your behalf it will look like this while it is provisioning:

![StackWizard5](doc/images/img6.png)

Once it has completed you'll see green text like below indicating that the work has been completed:

![StackWizard5](doc/images/img7.png)

Now that you have your environment created, you need to save the name of your S3 bucket for future use, you can find it by clicking on the `Outputs` tab and then looking for the resource `S3Bucket`, once you find it copy and paste it to a text file for the time being.

![StackWizard5](doc/images/img8.png)


## FAQ

**Q. How do I contribute my own example notebook?**

A. Although we're extremely excited to receive contributions from the community, we're still working on the best mechanism to take in examples from external sources. Please bear with us in the short-term if pull requests take longer than expected or are closed.
 
