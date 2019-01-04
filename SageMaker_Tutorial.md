# Getting Started with Amazon Forecast with Amazon SageMaker.

This guide will walk through the creation of a new SageMaker Notebook Instance, the configuration of IAM policies, an S3 bucket
and your first project with Amazon Forecast. The Notebook Instance can then be used again for additional exploratory work with 
Amazon Forecast.

## Creating Your Notebook Instance

First you will need to create a new Notebook Instance, to do that begin by logging into the AWS Console.

Next, ensure you are in the US-West-2 Region, do do that look in the top left corner, if it says `Oregon` next to support
that is correct, otherwise select `Oregon` from the drop-down.

Under `Find services` in the main body of the page, enter `SageMaker`, then select it from the drop-down.

To the left, will see a category titled `Notebook` inside that, click `Notebook instances`.

Click the orange `Create notebook instance` button.

Give the instance a name unique in the account you are using. If a shared account, place your name first like `ChrisKingForecastDemo`. The default Instance
type is fine. 

The Next component to change is the IAM role. Under the drop-down click `Create a new role`. Then for S3, select `Any S3 Bucket`, finally click `Create role`.
Note that the role itself has become a link. Open that link in a new tab.

Here you will update the policies of your instance to allow it to work with Forecast. Click the `Attach policies` button.

Next click the `Create policy` button at the top. In the new page, click the `JSON` tab.

Erase all of the content that is in the editor and paste the content in [IAM_Policy.json](IAM_Policy.json).

After pasting, click the `Review policy` button. Give the policy again a personalize name like `ChrisKingForecastIAMPolicy`.

For the description, enter in something about it being used to demo Forecast. Finally click `Create policy`. Close this tab or window.

Once closed you should see the tab for adding permissions to your SageMaker role. Click the `Filter Policies` link, then select
`Customer managed`. After that, you should see the policy you just created, if the list is long, just paste the name in the search bar to reduce the number
of items. If you do not see it still, click the refresh icon in the top right of the page.

After clicking the checkbox next to the policy, click `Attach policy` at the bottom of the page. Then close this window.

Back at the SageMaker Notebook Instance creation page, now click `Create notebook instance` at the bottom of the page. This process will take 5-10 minutes to complete. Once the status says `InService` you are ready to continue to the 
next session.

## Getting Started with Amazon Forecast.

To begin, click `Open Jupyter`, this will take you to the default interface for the Notebook Instance.

Click `New` then click `Terminal`, this will open a BASH shell for you on this instance. 

Enter the following commands to clone this repository onto this instance:

```
cd SageMaker
git clone https://github.com/aws-samples/amazon-forecast-samples.git
```

After that close your Terminal tab and go back to the main Notebook interface.

A new folder titled `amazon-forecast-samples` should be visible, click it, click notebooks, then click `Getting_started_with_Forecast-SageMaker.ipynb` this will open the notebook.

If prompted for a kernel, select `conda_python3`.

From here you will follow the instructions outlined in the notebook. 

**Read Every Cell FULLY Before Executing It**
