The purpose of these notebooks is to demonstrate the application of time series clustering techniques to split the target time series (TTS) data into homogenous chunks that *may* produce more accurate forecasts for the subsets of data when trained individually with the Forecast service. The intuition is that training Forecast models with clustered data will allow them to learn stronger patterns from homogenous subsets of the time series data. 

As risk of over-fitting exists with very high cluster counts, we set `num_clusters=3` with the intention of splitting the time series dataset into subsets of "fast moving", "slow moving", and "intermittent demand" items. Also, clustering techniques are not advised for datasets with fewer than a thousand time series since this could have limiting effect on deep learning models. 

We leverage the [tslearn.clustering](https://tslearn.readthedocs.io/en/stable/gen_modules/tslearn.clustering.html#module-tslearn.clustering) module of Python package [tslearn](https://github.com/tslearn-team/tslearn) for clustering the time series dataset using the [DTW Barycenter Averaging (DBA) KMeans](https://tslearn.readthedocs.io/en/stable/auto_examples/clustering/plot_kmeans.html#sphx-glr-auto-examples-clustering-plot-kmeans-py) algorithm with [Dynamic Time Warping (DTW)](https://en.wikipedia.org/wiki/Dynamic_time_warping) distance as the metric.

The collection includes two notebooks, the first is optional relating to data cleaning / processing; and the main notebook relating to time series clustering. We use the open source UCI [Online Retail II Data Set](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II) for this demonstration.

**Please note**, these notebooks cover the preprocessing and data preparation steps related to the clustering of Time Series data. The reader is referred to the [Forecast Developers Guide](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html) for model training and evaluation.

*Table of contents:*

- [01. Optional - Data Cleaning and Preparation](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Clustering_Preprocessing/01.%20Optional%20-%20Data%20Cleaning%20and%20Preparation.ipynb)
- [02. Time Series Clustering Using DTW KMeans](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Clustering_Preprocessing/02.%20Time%20Series%20Clustering%20Using%20DTW%20KMeans.ipynb)

*References:*

- Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
- https://archive.ics.uci.edu/ml/datasets/Online+Retail+II
- https://github.com/tslearn-team/tslearn
