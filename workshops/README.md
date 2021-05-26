## Workshops

- **[Pre-POC workshop](https://github.com/aws-samples/amazon-forecast-samples/tree/master/workshops/pre_POC_workshop)** is a hands-on, leave-in-place, guided learning (and demo) that is meant to accelerate a Forecast POC.  The workshop covers Best Practices for working with Amazon Forecast.  Targeted to Developers, Line-of-business, and Data Scientists who will be doing the execution work of a Forecast POC. 

  - The CloudFormation template configures all the AWS services (and permissions) to take data end-to-end through Forecast.  The Forecast section does not use notebook with manual waits between API calls anymore, instead users just copy their data to a S3 bucket that has a defined trigger to launch all the Forecast steps automatically.   

  #### **Three ways to use this workshop**

  1. **Self-service training.** You can bring your own data, and follow along all the steps below, starting with "Install the demo". You'll need time to customize the [Data Prep notebook to your data](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb). Best Practice theory is mixed-in along with Hands-on Lab instructions.
  2. **AWS- or AWS Partner-led training as a no-code, no-hands-on, canned demo**. [See the separate instructions](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/AWS_instructions.md) and look for notes about "canned demo". Follow the below instructions to "Install the demo" before day of your demo. The NYC Taxi demo will be created for you automatically. All you have to do is open AWS console to Amazon Forecast, and walk audience through the completed screens in the Forecast Dataset Group called "nyctaxi_weather_auto".
  3. **AWS- or AWS Partner-led hands-on, bring your own data, pre-POC workshop.** [See the separate instructions](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/AWS_instructions.md). For best results, ask for a sample of customer's anonymized POC data at least 1 week in advance. You'll need time to customize the [Data Prep notebook to their data](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/1.Getting_Data_Ready_nytaxi.ipynb). You'll also need follow the below instructions to "Install the demo" beforehand. Day of the workshop, share the customized Data Prep notebook with customer, so they can more quickly get going with their Forecast POC.

  - Data used:  NYC Taxi

  - Resources used:  

    - [Getting Started Guide and Best Practices Cheat Sheet Tutorial](https://github.com/aws-samples/amazon-forecast-samples/blob/master/ForecastCheatSheet.md)

    - [Improving Forecast Accuracy with Machine Learning Solution](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/pre_POC_workshop/install-forecast-solution.md)

      <br>

- **No code workshop** can be used in 2 ways:

  - [**Introduction demo**](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/no_code_workshop/forecast-with-console.md).  Developers and Line-of-business folks can follow-along this markdown file to learn start-to-finish how to create forecasts.  100% no-code, through UI screens using console only.  
  - **[Notebook using Amazon Forecast Python SDK](https://github.com/aws-samples/amazon-forecast-samples/blob/master/workshops/no_code_workshop/forecast-with-api-completed.ipynb)** to make API calls, with manual waits between each API call, to perform exactly the same tasks as the 100% no-code demo.  Targeted at Integration Partners, MLOps Engineers, and Developers responsible for putting forecasts into production.
  - Data used:  Energy consumption

- Immersion Day Workshop is an older version of the No code workshop notebook portion.

<br>


## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
