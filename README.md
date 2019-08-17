## Amazon Forecast Samples

This repository contains examples that show how to use the various features of [Amazon Forecast](https://aws.amazon.com/forecast/). 

[Forecast developer guide](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html)

## Examples
### Introduction 
These examples include a general introduction to the service and introduces the main APIs in a self-guided fashion.  

* [Getting started](notebooks) runs a household power consumption dataset through Amazon Forecast. 

## Building Your Environment

As mentioned above, the first step is to deploy a CloudFormation template that will perform much of the initial setup for you. In another browser window login to your AWS account. Once you have done that open the link below in a new tab to start the process of deploying the items you need via CloudFormation.

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=ForecastDemo&templateURL=https://chriskingpartnershare.s3.amazonaws.com/PersonalizeDemo.yaml)


## FAQ
_What do I need to get started?_  
 The quickest set up to run example notebook includes:   
 
 
 * An AWS account
 * Proper IAM User and role setup
 * An S3 bucket where your data is stored

_How do I contribute my own example notebook?_  
 Although we're extremely excited to receive contributions from the community, we're still working on the best mechanism to take in examples from external sources. Please bear with us in the short-term if pull requests take longer than expected or are closed.
 
 _How do I use control AWS Forecast resources using the aws cli?_

  You can clone or download this repository and run `aws configure add-model --service-model [MODEL_JSON_FILE]`
 on the files in `sdk`, eg `aws configure add-model --service-model file://forecast-2019-07-22.normal.json`
 
 ## Contact us
 Contact the dev team @ forecastpreview-support@amazon.com


