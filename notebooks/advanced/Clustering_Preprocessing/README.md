The purpose of these notebooks is to demonstrate the application of time series clustering techniques to split the target time series (TTS) data into homogenous chunks that *may* produce more accurate forecasts for the subsets of data when trained individually with the Forecast service. The intuition is that training Forecast models with clustered data will allow them to learn stronger patterns from homogenous subsets of the time series data. 

We provide examples of several time series clustering techniques:
 1. Based on [tslearn.clustering](https://tslearn.readthedocs.io/en/stable/gen_modules/tslearn.clustering.html#module-tslearn.clustering) module of Python package [tslearn](https://github.com/tslearn-team/tslearn) for clustering the time series dataset using the [DTW Barycenter Averaging (DBA) KMeans](https://tslearn.readthedocs.io/en/stable/auto_examples/clustering/plot_kmeans.html#sphx-glr-auto-examples-clustering-plot-kmeans-py) algorithm with [Dynamic Time Warping (DTW)](https://en.wikipedia.org/wiki/Dynamic_time_warping) distance as the metric.
 2. Based on [sklearn.cluster](https://scikit-learn.org/stable/modules/clustering.html) module of Python package [scikit-learn](https://github.com/scikit-learn/scikit-learn) for clustering tabular dataset using the [K-means](https://scikit-learn.org/stable/modules/clustering.html#k-means) algorithm. To transform Time Series data into usual tablar data we are using [TSFresh](https://tsfresh.readthedocs.io/en/latest/) python package. It automatically calculates a large number of time series characteristics, the so called features. 

 Dataset:
 We use the open source UCI [Online Retail II Data Set](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II) for this demonstration.

The collection includes 3 notebooks:
1. [01. Optional - Data Cleaning and Preparation](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Clustering_Preprocessing/01.%20Optional%20-%20Data%20Cleaning%20and%20Preparation.ipynb) is optional relating to data cleaning / processing
2. [02. Time Series Clustering Using DTW KMeans](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Clustering_Preprocessing/02.%20Time%20Series%20Clustering%20Using%20DTW%20KMeans.ipynb) is relating to time series clustering. 
3. [03. Time Series Clustering using TSFresh + KMeans](https://github.com/aws-samples/amazon-forecast-samples/blob/master/notebooks/advanced/Clustering_Preprocessing/03.%20Time%20Series%20Clustering%20using%20TSFresh%20%2B%20KMeans.ipynb)

**Please note**, these notebooks cover the preprocessing and data preparation steps related to the clustering of Time Series data. The reader is referred to the [Forecast Developers Guide](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html) for model training and evaluation.

*References:*

- Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
- https://archive.ics.uci.edu/ml/datasets/Online+Retail+II
- https://github.com/tslearn-team/tslearn
- https://github.com/scikit-learn/scikit-learn
- https://tsfresh.readthedocs.io/en/latest/
