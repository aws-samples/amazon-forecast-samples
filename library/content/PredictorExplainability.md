
## Interpreting predictor explainability

[Predictor Explainability](https://docs.aws.amazon.com/forecast/latest/dg/predictor-explainability.html) helps to understand how the attributes in your related-time-series and item metadata [datasets](Datasets.md), such as price, category, or holidays, impact your forecast values. Forecast uses a metric called impact scores to quantify the relative impact of each attribute and determine whether they generally increase or decrease forecast values.

Impact scores measure the relative impact attributes have on forecast values. For example, if the  `price`  attribute has an impact score that is twice as large as the  `brand_id`  attribute, you can conclude that the price of an item has twice the impact on forecast values than the product brand. Impact scores also provide information on whether an attribute increases or decreases the forecasted value. A negative impact score reflects that the attribute tends to decrease the value of the forecast.

Impact scores measure the relative impact of attributes to each other, not the absolute impact. If an attribute has a low impact score, that doesn’t necessarily mean that it has a low impact on forecast values; it means that it has a lower impact on forecast values than other attributes used by the predictor. If you change attributes in your predictor, the impact scores may differ, and the attribute with the low impact score may have a higher score relative to other attributes.

You can’t use impact scores to determine whether particular attributes improve the model accuracy or not.  You should use [accuracy metrics](https://docs.aws.amazon.com/forecast/latest/dg/metrics.html) such as weighted quantile loss and others provided by Forecast to access predictor accuracy.

Explainability is available through the [AutoPredictor](AutoPredictor.md) models by enabling it during model creation or enabling it after the fact.  Once computed, you may view the outcome visually, as in Figure 1, through the AWS Console.  You may also request for data to be exported in a tabular output as well.

***Figure 1 - Example of Explainability available inside the AWS Console***
<br>
![Explainability](../images/predictor-explainability.png)

<br><br>
[Return to Table of Contents](../README.md)
