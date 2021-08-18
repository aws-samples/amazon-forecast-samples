"""Data preparation utilities for Amazon Forecast pre-PoC workshop
"""

# Python Built-Ins:
from typing import List

# External Dependencies:
import pandas as pd

# Local Dependencies:
from .analysis import analyze_lengths_and_sparsity


def select_by_df(source_df: pd.DataFrame, condition_df: pd.DataFrame) -> pd.DataFrame:
    """Select elements from source_df matching records in condition_df for shared columns

    Arguments
    ---------
    source_df : pd.DataFrame
        Dataframe to select from
    condition_df : pd.DataFrame
        Selection criteria dataframe. Columns should be a subset of `source_df`. Records should
        ideally be unique for performance purposes but don't have to be. Index is ignored.

    Returns
    -------
    result : pd.DataFrame
        Filtered records from `source_df` matching `condition_df`
    """
    return source_df[
        source_df[condition_df.columns].isin(condition_df.to_dict(orient="list")).all(axis=1)
    ]


def aggregate_time_series(
    input_df: pd.DataFrame,
    agg_freq: str,
    timestamp_col: str,
    target_col: str,
    dimension_cols: List[str],
    agg_dict: dict,
    already_grouped: bool=False,
    analyze: bool=True,
) -> pd.DataFrame:
    """Aggregate pandas dataframe to a given time frequency
    
    Expects a timestamp and item_id column as time series dimensions. If additional columns are
    present, you need to put them in the agg_dict to specify grouping function per additional
    column.

    Arguments
    ---------
    input_df : pd.DataFrame
        Input dataframe
    agg_freq : str
        Time frequency for grouping. Can be "Y", "M", "W", "D", "H", "T" as per the `freq` param
        of: https://pandas.pydata.org/docs/reference/api/pandas.Grouper.html
    timestamp_col : str
        Column name of `input_df` where record timestamps are located
    target_col : str
        Column name of `input_df` where the target variable for forecasting is located
    dimension_cols : List[str]
        List of column names identifying separate timeseries (e.g. ['item_id', 'location'])
    agg_dict : dict
        dictionary of non-key columns with each column's desired aggregation function per pandas.
        For example: `{ "Qty":"sum", "location_id":"first", ...}`
    already_grouped : bool
        Set True if input_df is already grouped by timestamp at the desired aggregation level.
        Default False
    analyze : bool
        Set False to disable analysis & plotting of timeseries sparsity after the aggregation.
        Default True

    Returns
    -------
    result : pd.DataFrame
        Aggregated dataframe
    """
    print(f"agg_freq='{agg_freq}'")
    g = input_df.copy()
    
    if not already_grouped:
        # aggregate by agg_freq
        g = g.groupby(
            [pd.Grouper(key=timestamp_col, freq=agg_freq), *dimension_cols]
        ).agg(agg_dict)
        g.drop_duplicates(inplace=True)

        g.reset_index(inplace=True)
        print(f"grouped shape = {g.shape}, original shape = {input_df.shape}")
        display(g.sample(5))
    else:
        print("already grouped: no-op")

    if analyze:
        analyze_lengths_and_sparsity(
            g,
            agg_freq=agg_freq,
            timestamp_col=timestamp_col,
            forecast_dims=dimension_cols,
            target_col=target_col,
        )

    return g
