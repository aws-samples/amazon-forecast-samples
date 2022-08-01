## Providing Data for your newly deployed project

You may repeat this process as a quick start for each use case you intend to deploy.  Since each deployment is mutually exclusive from the other, you can operate each stack independently.

In the prior step at the [Solution Guidance](SolutionGuidance.md) stack creation, a **S3Bucket**  and **StackName** parameter were provided.

This step guides how to deposit files on S3 in a structure the deployment is expecting.  

1. If you are using the provided sample dataset, download [Food Demand](https://amazon-forecast-samples.s3.us-west-2.amazonaws.com/ml_ops/FoodDemand.zip) to your laptop and unzip the file which will create three files (RTS, TTS, Item metadata) inside three directories.

2. In the AWS Console, navigate to the S3 service.  You can do this by typing S3 in the "search for services" control in the black menu bar and hitting enter.

3. Once in S3, account buckets are listed.   Click on the bucket name you provided in the prior section to open the bucket.

4. Once inside this bucket, it will be empty.  You will click "Create Folder" and provide the same string as your **StackName**.

5. Next, click on the orange Upload button.

6. Drag the three folders from your laptop and drop them in the S3 window waiting the upload.

7. You should see 3 files in the list of files and folders.  Click on Upload at the bottom of this page.

8. Once the upload is complete, your AWS Console should look like this screenshot below.  In the example, the StackName is aiml42.
<br><br>
![S3 Upload](../images/s3-inputs.jpg)
<br><br>

NEXT: Now it's time to build your [Amazon Forecast Dataset Group](DatasetGroup.md).