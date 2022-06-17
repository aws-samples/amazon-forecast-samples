
# AWS supplied dataset: Weather Index

The Amazon Forecast Weather Index is a built-in featurization that incorporates historical and projected weather information into your model.  It is especially useful for retail use cases, where temperature and precipitation can significantly affect product demand.

When the Weather Index is enabled, Forecast applies the weather featurization only to time series where it finds improvements in accuracy during predictor training.  If supplementing a time series with weather information does not improve its predictive accuracy during backtesting, Amazon Forecast does not apply the Weather Index to that particular time series.

To apply the Weather Index, you must 

 - include a  [geolocation attribute](https://docs.aws.amazon.com/forecast/latest/dg/weather.html#adding-geolocation)  in your target time series dataset and any related time series datasets.  
 - specify  [time zones](https://docs.aws.amazon.com/forecast/latest/dg/weather.html#specifying-timezones)  for your target time-series timestamps.

For more information regarding dataset requirements, see  [Conditions and Restrictions](https://docs.aws.amazon.com/forecast/latest/dg/weather.html#weather-conditions-restrictions).

**For a more comprehensive list of considerations, visit the [weather index](https://docs.aws.amazon.com/forecast/latest/dg/weather.html#adding-geolocation) page.**


<br><br>
[Return to Table of Contents](../README.md)
