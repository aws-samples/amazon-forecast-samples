## Outbrain Revenue Forecast

A POC to forecast Outbrain revenues using [Amazon Forecast](https://aws.amazon.com/forecast/). 

See the POC Inception [Algorithmically optimize the position of Outbrain vs Recs](https://cnissues.atlassian.net/wiki/spaces/FP/pages/609550359/Algorithmically+optimize+the+position+of+Outbrain+vs+Recs+based+on+RPM+R.A.T.+Inception)

## Agenda

The steps below outline the process of building the time-series prediction models, evaluating them, and then cleaning
 up the resources. To get started execute the following steps.

1. Deploy the CloudFormation Template below or build a local Jupyter environment with the AWS CLI installed and configured for your IAM account.
1. `1.Getting_Data_Ready.ipynb` - Guides you through preparing the Outbrain dataset to be used with Amazon Forecast.
1. `2.Building_Your_Predictor.ipynb` - Explains how to use the dataset prepared to build the models.
1. `3.Evaluating_Your_Predictor.ipynb` - Takes the models just created and evaluates its performance against real
 observed measurements.

Each notebook can be found within the `notebooks` folder in this project.

## Outline

1. First deploy a CloudFormation template that will create an S3 bucket for data storage, a SageMaker Notebook Instance where the exercises are executed, IAM policies for the Notebook Instance, and it will clone this repository into the Notebook Instance so you are ready to get started.
1. Next open the `Getting_Data_Ready.ipynb` to get started.
1. This notebook will guide you through the process of the other notebooks until you have a working and evaluated forecast.

Note that we are using the `CNI-Experimental` AWS account for the POC evaluation. 

## Development

- See the [Project Structure](PROJECTSTRUCTURE.md) documentation 
- See the [Makefile](Makefile) commands
  - Use `make create_environment` to create a py virtual environment
  - Use `make requirements` to install the requirements
  - take a look at the other commands

See the [Amazon Forecast developer guide](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html)

### Data

- Recreate dataset: `make dataset`  
- Synch data from s3: `make sync_data_from_s3`
- Synch data to s3: `make sync_data_to_s3`

---

<p><small> Note that this repository is a fork of https://github.com/aws-samples/amazon-forecast-samples
 integrated with the project structure based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter
 -data-science
/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>



