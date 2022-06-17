
# Target Time Series (TTS)

In Amazon Forecast, historical event data is called the Target Time Series (TTS).  This the only required dataset type required to do forecasting and contains the signal for which you want to produce a future-dated forecast. 
<br>
TTS consists of:
  - An **"item_id", which is a unique identifier for the things you want to forecast**.  The unique identifier can represent distinct products, services, KPI measures/metrics, geography, customers and more.  The field can be a concatenation of fields to form a unique time series identifier.  You may also define dimensions to prevent the need to concatenate.  This feature communicates "*what*".
  - Also a **"timestamp" when the historical event occurred**.  Two timestamp formats are supported, as illustrated in Figure 1.  If you are forecasting below daily grain, you will need to provide timestamps with HH:mm:ss precision.  This feature communicates "*when*".
  - And a **"target_value" that expresses the quantity of the event**.  These continuous values can be integer or decimal (float) numbers.  This feature communicates "*how much*".

In addition, you may specify up to 10 columns that provided added dimensions for more granularity.  An example is shown in Figure 1, where in addition to item_id, a store number is specified.   You may define these according to your hierarchy as needed.

***Figure 1 - Example of TTS with sample data records***
<br>
![TTS](../images/target-time-series.png)

You are able to define your TTS with JSON; this example supports the Figure 1 schema.
```
{
  "Attributes": [
    {
      "AttributeName": "store_id",
      "AttributeType": "string"
    },
    {
      "AttributeName": "item_id",
      "AttributeType": "string"
    },
    {
      "AttributeName": "target_value",
      "AttributeType": "integer"
    },
    {
      "AttributeName": "timestamp",
      "AttributeType": "timestamp"
    }
  ]
}
```



<br><br>
[Return to Datasets](./Datasets.md)
[Return to Table of Contents](../README.md)
