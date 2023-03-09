## Amazon Forecast End-to-End Deployments CD pipeline

This is a sample code repository for demonstrating how you can organize your code for deploying a complete end-to-end workflow with CodeCommit, CodePipeline and CodeBuild. The CloudFormation templates you will use are from [Amazon Forecast End-to-End Deployments Made Simple](https://github.com/aws-samples/amazon-forecast-samples/tree/main/ml_ops). 

The example uses [Food Demand](https://github.com/aws-samples/amazon-forecast-samples/blob/main/ml_ops/sample_data/FoodDemand.md) configuration to demonstrate Amazon Forecast solutions deployment. 

This code repository defines the CloudFormation templates which define the Step functions, Lambda functions, and AWS Systems Manager, etc as infrastructure. It also has configuration files associated with `staging` and `prod` stages. 

Upon triggering a deployment, the CodePipeline pipeline will deploy two Forecast solutions - `staging` and `prod`. After the first deployment is completed, the CodePipeline waits for a manual approval step for promotion to the prod stage. You will need to go to CodePipeline AWS Managed Console to complete this step.

You own this code and you can modify this template to change as you need it, add additional tests for your custom validation. 

A description of some of the artifacts is provided below:


## Layout of the Seed Forecast Project Template

`buildspec.yml`
 - this file is used by the CodePipeline's Build stage to build CloudFormation templates.

`forecast-mlops-dependency.yml`
 - this CloudFormation template file is packaged by the build step in the CodePipeline and is deployed in different stages. It is built for creating Amazon S3 buckets, Lambda functions and IAM permissions for the following orchestration workload. The description of the template can be found [here](https://github.com/aws-samples/amazon-forecast-samples/tree/main/ml_ops)

`forecast-mlops-solution-guidance.yml`
 - this CloudFormation template file is packaged by the build step in the CodePipeline and is deployed in different stages. It creates Step functions which help coordinate the machine learning pipelines which orchestrate all the Amazon Forecast processes for each workload. The description of the template can be found [here](https://github.com/aws-samples/amazon-forecast-samples/tree/main/ml_ops)

`staging-dep-config.json`
 - this configuration file is used to customize dependency of `staging` stage in the pipeline. You can configure the Amazon S3 bucket.

`staging-config.json`
 - this configuration file is used to customize `staging` stage in the pipeline. You can configure the Amazon Forecast solution here.

`prod-dep-config.json`
 - this configuration file is used to customize dependency of `prod` stage in the pipeline. You can configure the Amazon S3 bucket.

`prod-config.json`
 - this configuration file is used to customize `prod` stage in the pipeline. You can configure the Amazon Forecast solution here.
