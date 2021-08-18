"""Timeseries analysis utilities for Amazon Forecast pre-PoC workshop
"""

# Python Built-Ins:
from typing import Iterable, Optional

# External Dependencies:
from IPython.display import display
from matplotlib import pyplot as plt
import pandas as pd

# Local Dependencies:
from . import distributed


def analyze_lengths_and_sparsity(
    binned_df: pd.DataFrame,
    agg_freq: str,
    timestamp_col: str,
    forecast_dims: Iterable[str],
    target_col: str,
    hist_bins: int=32,
    dense_threshold_quantile: float=0.75,
):
    """Inspect the distribution of time-series length identify 'dense' and 'sparse' time-series

    TODO: Check this works when additional columns are present

    Expects a timestamp and item_id column as time series dimensions.

    Arguments
    ---------
    binned_df : pd.DataFrame
        Input dataframe already binned/aggregated by the timestamp field at the desired frequency
    agg_freq : str
        Time frequency for grouping (Only used for labelling plots). Can be as per the `freq` param
        of: https://pandas.pydata.org/docs/reference/api/pandas.Grouper.html
    timestamp_col : str
        Column name of `input_df` where record timestamps are located
    forecast_dims : str
        Column name of `input_df` where each record's forecast item identifier is located
    target_col : str
        column name of `input_df` where the target variable for forecasting is located
    hist_bins : int
        Number of bins to draw on the main histograms (zoomed histogram will halve this)
    dense_threshold_quantile : float
        Percentage of highest-datapoint-count timeseries (i.e. 0 = 0% to 1.0 = 100%) to treat as
        'dense'

    Returns
    -------
    dense : pd.Series
        Number of data points, indexed by identifying dimensions (e.g. item ID, location, etc) for
        "dense" time-series only.
    dense : pd.Series
        Number of data points, indexed by identifying dimensions (e.g. item ID, location, etc) for
        "sparse" time-series only.
    """
    print("Analyzing timeseries length and sparsity")
    
    # INSPECT DISTRIBUTION OF TIME SERIES LENGTH
    # In chart below, you want bulk of distribution to sit after 300-mark on x-axis.
    # If bulk of distribution is bunched closer to 0, choose smaller time granularity or aggregate item-level only

    # num data points per item
    sparsity = binned_df.groupby(forecast_dims).count().sort_values(target_col, ascending=False)
    sparsity[[target_col]].hist(bins=hist_bins);
    plt.title("Count number of data points per item");
    plt.suptitle("In chart below, you want bulk of distribution to sit after 300-mark on x-axis.")
    
    sparsity_stats = sparsity[target_col].describe()
    print("Data point count statistics:")
    print(sparsity_stats)
    density_threshold = sparsity[target_col].quantile(dense_threshold_quantile)
    print(f"Dense threshold {dense_threshold_quantile:.2%} is at {density_threshold} data points")

    # In chart below, you want to see the shape of a distribution (counts usually negative-binomial)
    # You do not want to see a randomly uniform shape
    value_stats = binned_df[target_col].describe()

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle("In chart below, you want to see a distribution, usually negative-binomial or gaussian.", y=1.08)
    # plot distribution of target_value itself
    binned_df[[target_col]].hist(bins=hist_bins, ax=axs[0])
    axs[0].set_title(f"Distribution of {target_col} at '{agg_freq}' level", y=1.08);

    # zoom-in plot distribution of target_value itself
    binned_df.loc[
        (binned_df[target_col] < (2 * value_stats['75%'])),
        :,
    ][[target_col]].hist(bins=int(hist_bins / 2), ax=axs[1])
    axs[1].set_title(f"Distribution of {target_col} up to 75% percentile", y=1.08);

    # Return forecast dimension combinations mapped to their number of data points:
    is_dense = sparsity[target_col] >= density_threshold
    return (
        sparsity[is_dense][target_col].copy(),
        sparsity[~is_dense][target_col].copy(),
    )


def _get_time_min_max(the_df, item_id_col, timestamp_col, location_id_col=None):
    """Calculate min timestamp, max timestamp per item and/or per item-location time series  
       Inputs: pandas dataframe with columns: timestamp, target_value, item_id, location_id (optional)
       Outputs: pandas dataframe with 2 extra columns "min_time" and "max_time"
    """
    df = the_df.copy()
    
    if location_id_col is None:
        # get max
        max_time_df = \
            df.groupby([item_id_col], as_index=False).max()[[item_id_col, timestamp_col]]
        max_time_df.columns = [item_id_col, 'max_time']
        # get min
        min_time_df = df.groupby([item_id_col], as_index=False).min()[[item_id_col, timestamp_col]]
        min_time_df.columns = [item_id_col, 'min_time']
        # merge 2 extra columns per item grouping: max and min
        df = df.merge(right=max_time_df, on=item_id_col)
        df = df.merge(right=min_time_df, on=item_id_col)
        
    else:
        # get max
        max_time_df = \
            df.groupby([item_id_col, location_id_col], as_index=False).max()[[item_id_col, location_id_col, timestamp_col]]
        max_time_df.columns = [item_id_col, location_id_col, 'max_time']
        # get min
        min_time_df = df.groupby([item_id_col, location_id_col], as_index=False).min()[[item_id_col, location_id_col, timestamp_col]]
        min_time_df.columns = [item_id_col, location_id_col, 'min_time']
        # merge 2 extra columns per item grouping: max and min
        df = df.merge(right=max_time_df, on=[item_id_col, location_id_col])
        df = df.merge(right=min_time_df, on=[item_id_col, location_id_col])
        
    return df


def _get_velocity_per_item(the_df, timestamp_col, target_value_col, item_id_col, location_id_col=None):
    """Calculate velocity as target_demand per time unit per time series
       Inputs: pandas dataframe with columns: timestamp, target_value, item_id, location_id (optional)
       Outputs: pandas dataframe with extra "velocity" column
    """
    df = the_df.copy()
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], format='%Y-%m-%d %H:%M:%S')
    
    # append 2 extra columns per time seres: min_time, max_time
    if location_id_col == None:
        df = _get_time_min_max(the_df, item_id_col, timestamp_col)
    else:
        df = _get_time_min_max(the_df, item_id_col, timestamp_col, location_id_col)
        
#     print (df.sample(10))
    
    # calculate time span per time seres
    df['time_span'] = df['max_time'] - df['min_time']
    df['time_span'] = df['time_span'].apply(lambda x: x.seconds / 3600 + 1) # add 1 to include start datetime and end datetime
    
    # calculate average item demand per time unit
    if location_id_col is None:
        df = df.groupby([item_id_col], as_index=False).agg({'time_span':'mean', target_value_col:'sum'})
    else:
        df = df.groupby([item_id_col, location_id_col], as_index=False).agg({'time_span':'mean', target_value_col:'sum'})
    df['velocity'] = df[target_value_col] / df['time_span']
    
    return df


def get_top_moving_items(
    df: pd.DataFrame,
    timestamp_col: str,
    target_value_col: str,
    item_id_col: str,
    location_id_col: Optional[str]=None,
) -> pd.DataFrame:
    """Calculate mean velocity (demand per unit time) over all time series.

    Returns
    -------
    top_movers : pd.DataFrame
        Dataframe indexed by the forecast dimension columns (item_id_col and location_id_col if
        provided); with 'velocity' column measuring velocity. Sorted descending by 'velocity' and
        including only the top movers.
    slow_movers : pd.DataFrame
        Dataframe indexed by the forecast dimension columns (item_id_col and location_id_col if
        provided); with 'velocity' column measuring velocity. Sorted descending by 'velocity' and
        including only the slow movers.
    """
    df_velocity = _get_velocity_per_item(
        df.copy().reset_index(drop=True),
        timestamp_col,
        target_value_col,
        item_id_col,
        location_id_col,
    )
    criteria = df_velocity["velocity"].mean()
    print("average velocity of all items:", criteria)
    df_velocity["top_moving"] = df_velocity["velocity"] > criteria

    dims_except_timestamp = [item_id_col] + ([location_id_col] if location_id_col else [])
    # TODO: I think this could be simplified to remove the branch?
    if location_id_col:
        num_top = df_velocity.loc[
            (df_velocity.top_moving==True), :
        ].groupby(dims_except_timestamp).first().shape[0]
        num_slow = df_velocity.loc[
            (df_velocity.top_moving==False), :
        ].groupby(dims_except_timestamp).first().shape[0]
        num_time_series = df.groupby(dims_except_timestamp).first().shape[0]
    else:
        num_top = df_velocity.loc[(df_velocity.top_moving==True), item_id_col].nunique()
        num_slow = df_velocity.loc[(df_velocity.top_moving==False), item_id_col].nunique()
        num_time_series = df[item_id_col].nunique()

    print(f"Found {num_top} top-moving time series ({num_top / num_time_series:.2%} of total)")
    print(
        f"Found {num_slow} slow-moving time series ({num_slow / num_time_series:.2%} of total)\n"
    )

    # TODO: Why did the original df_ts_velocity variant skip the sort?
    top_moving = df_velocity.loc[(df_velocity.top_moving==True), :].sort_values("velocity", ascending=False).copy()
    slow_moving = df_velocity.loc[(df_velocity.top_moving==False), :].sort_values("velocity", ascending=False).copy()

    print("Top moving:")
    display(top_moving.head(3))
    print("\nSlowest moving:")
    display(slow_moving.tail(3))

    # We could do these aggregations above, but leaving them til here gives more detailed displays:
    return (
        top_moving.groupby(dims_except_timestamp)[
            ["velocity"]
        ].first().sort_values("velocity", ascending=False),
        slow_moving.groupby(dims_except_timestamp)[
            ["velocity"]
        ].first().sort_values("velocity", ascending=False),
    )


def classify_one_timeseries(
    s_df: pd.DataFrame,
    time_col: str,
    target_col: str,
    adi_col: str="ADI",
    cv2_col: str="CV_square",
    output_col: str="ts_type",
):
    """Classify time-series by demand behavior type from historical data

    Series are classified by their calculated Average Demand Interval (ADI) and the square of their
    Coefficient of Variation (CV).

    Using definitions given at: https://frepple.com/blog/demand-classification/
    Original article available at: https://robjhyndman.com/papers/idcat.pdf

    Classifying rules:

    1. 'smooth' demand if ADI < 1.32 and CV² < 0.49 (and as default, if checks fail)
    2. 'intermittent' demand if ADI >= 1.32 and CV² < 0.49
    3. 'erratic' demand if ADI < 1.32 and CV² >= 0.49
    4. 'lumpy' (largely unforecastable) demand if ADI >= 1.32 and CV² >= 0.49

    Arguments
    ---------
    s_df : pd.DataFrame
        Dataframe already filtered to a single timeseries
    time_col : str
        Input column name of `s_df` where the record timestamps are stored
    target_col : str
        Input column name of `s_df` where the demand/target variable is stored
    adi_col : str
        Column name of `s_df` where the ADI scores should be stored. Default 'ADI'
    cv2_col : str
        Column name of `s_df` where the squared CV scores should be stored. Default 'CV_square'
    output_col : str
        Column name of `s_df` where the classification label should be stored. Default 'ts_type'

    Returns
    -------
    result : pd.DataFrame
        Copy of `s_df` modified to add labels at `output_col`, ADI scores at `adi_col`, CV² scores
        at `cv2_col`.
    """
    df = s_df.copy()
    
    # Calculate ADI:
    num_periods = df[time_col].nunique()
    num_demands_missing = df[target_col].isna().sum()
    num_demands = num_periods - num_demands_missing
    ADI = num_periods / num_demands if num_demands else float("inf")
    df[adi_col] = ADI
    
    # Calculate CV, coefficient of variation = std of population / mean value of population
    CV = df[target_col].std() / df.loc[(df[target_col]>0), target_col].mean()
    CV_square = CV * CV
    df[cv2_col] = CV_square
    
    # Apply classification rules:
    df[output_col] = "smooth"
    if ((ADI < 1.32) & (CV_square < 0.49)):
        df[output_col] = "smooth"
    elif ((ADI >= 1.32) & (CV_square < 0.49)):
        df[output_col] = "intermittent"
    elif ((ADI < 1.32) & (CV_square >= 0.49)):
        df[output_col] = "erratic"
    elif ((ADI >= 1.32) & (CV_square >= 0.49)):
        df[output_col] = "lumpy"

    return df


def classify_timeseries_set(
    df: pd.DataFrame,
    time_col: str,
    target_col: str,
    item_id_col: str,
    other_dimension_cols: Iterable[str]=[],
    adi_col: str="ADI",
    cv2_col: str="CV_square",
    output_col: str="ts_type",
    num_dask_partitions: int=1,
    use_dask_if_available: bool=True,
):
    """Classify time-series by demand behavior type from historical data

    Series are classified by their calculated Average Demand Interval (ADI) and the square of their
    Coefficient of Variation (CV).

    Using definitions given at: https://frepple.com/blog/demand-classification/
    Original article available at: https://robjhyndman.com/papers/idcat.pdf

    Classifying rules:

    1. 'smooth' demand if ADI < 1.32 and CV² < 0.49 (and as default, if checks fail)
    2. 'intermittent' demand if ADI >= 1.32 and CV² < 0.49
    3. 'erratic' demand if ADI < 1.32 and CV² >= 0.49
    4. 'lumpy' (largely unforecastable) demand if ADI >= 1.32 and CV² >= 0.49

    Arguments
    ---------
    df : pd.DataFrame
        Dataframe containing multiple time-series already aggregated to correct time frequency.
    time_col : str
        Input column name of `df` where the record timestamps are stored
    target_col : str
        Input column name of `df` where the demand/target variable is stored
    item_id_col : str
        Input column name of `df` where the item IDs are stored
    other_dimension_cols : Iterable[str]
        Any other columns of `df` describing dimensions on which the forecast should be split out
        (such as location ID, etc). Default []
    adi_col : str
        Column name of `df` where the ADI scores should be stored. Default 'ADI'
    cv2_col : str
        Column name of `df` where the squared CV scores should be stored. Default 'CV_square'
    output_col : str
        Column name of `df` where the classification label should be stored. Default 'ts_type'
    num_dask_partitions : int
        See `distributed.suggest_num_dask_partitions()` for guidance on setting this. Ignored if
        dask is not used.
    use_dask_if_available : bool
        Set `False` to disable distributing the computation with Dask, even if Dask is installed.
        Default True

    Returns
    -------
    result : pd.DataFrame
        Copy of `df` modified to add labels at `output_col`, ADI scores at `adi_col`, CV² scores at
        `cv2_col`.
    """
    # For Dask distributed we need to know the output shape (dtypes) of our apply() function:
    output_meta = df.iloc[0:0].copy()
    output_meta[adi_col] = 0.0
    output_meta[cv2_col] = 0.0
    output_meta[output_col] = "tmp"

    # Do df.groupby().apply() with Dask if available & configured:
    return distributed.group_and_apply(
        df,
        group_by_cols=[item_id_col] + other_dimension_cols,
        apply_fn=lambda g: classify_one_timeseries(
            g,
            time_col=time_col,
            target_col=target_col,
            adi_col=adi_col,
            cv2_col=cv2_col,
            output_col=output_col,
        ),
        output_meta=output_meta,
        num_dask_partitions=num_dask_partitions,
        use_dask_if_available=use_dask_if_available,
    ).reset_index([item_id_col] + other_dimension_cols, drop=True)
