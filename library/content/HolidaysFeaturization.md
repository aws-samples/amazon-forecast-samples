
# AWS supplied dataset: Holidays Featurizations

For customers who experience changes in their operations around holidays, Amazon Forecast provides a built-in featurization that incorporates a feature-engineered dataset of national holiday information.

To apply the Holidays Featurizations, simply specify an additional dataset declaration when creating a [Predictor](./AutoPredictor.md) as follows:
<br>

```
      "DataConfig": {          
        "AdditionalDatasets": [          
            {             
                "Name": "holiday",            
                "Configuration": {
                    "CountryCode" : ["US"]
                }      
            },      
          ]   
        }, 
```


**For a more comprehensive list of considerations, visit the [holidays featurization](https://docs.aws.amazon.com/forecast/latest/dg/holidays.html) page.**


<br><br>
[Return to Table of Contents](../README.md)
