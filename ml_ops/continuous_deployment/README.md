## Amazon Forecast End-to-End Deployments CD pipeline

This solution is to demo how to orchestrate the the continuous deployment (CD) of Amazon Forecast solutions using CodeCommit, CodePipeline, CodeBuild and CloudFormation. You will use the CloudFormation templates created in [Amazon Forecast End-to-End Deployments Made Simple](https://github.com/aws-samples/amazon-forecast-samples/tree/main/ml_ops) to deploy Forecast MLOps workflows.


To begin with, you need to create a zip file which contains seed code and upload to Amazon S3.
```bash
LOCAL_PATH=forecast-mlops-workflow.zip
S3_BUCKET=<your-s3-bucket>

(cd seed && zip -r ../${LOCAL_PATH} * )
aws s3 cp ${LOCAL_PATH} s3://${S3_BUCKET}/cfn/forecast-mlops-workflow.zip
```

Then you can run the following bash code to deploy the solution.
```bash
REGION=<your-region>
STACK_NAME=mlops-forecast-infra
CFN_FILE=forecast_deploy_cfn.yaml
SeedCodeS3Bucket=${S3_BUCKET}
SeedCodeS3Key=cfn/forecast-mlops-workflow.zip

aws cloudformation deploy --region ${REGION} \
							--stack-name ${STACK_NAME} \
							--template-file ${CFN_FILE} \
							--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
							--parameter-overrides SeedCodeS3Bucket=${SeedCodeS3Bucket} \
								SeedCodeS3Key=${SeedCodeS3Key}
```

## Move to Production

1. You need to revisit and refine the roles and permissions created in CloudFormation templates to align with your security policies. 
2. It's recommended to refine data ingestion Amazon S3 structures so that you are able to ingest data in incremental fashion.
3. You should consider enabling [Amazon Forecast predictor monitoring](https://aws.amazon.com/blogs/machine-learning/continuously-monitor-predictor-accuracy-with-amazon-forecast/) in your Prod deployment, so you will have more information to determine and improve retraining strategy.
4. You can refer to the workshop [Building a Cross-account CI/CD Pipeline](https://catalog.us-east-1.prod.workshops.aws/workshops/00bc829e-fd7c-4204-9da1-faea3cf8bd88/en-US/) for multi-accounts deployment.