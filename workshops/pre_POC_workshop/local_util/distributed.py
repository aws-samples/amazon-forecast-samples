"""Distributed/parallelized utilities speeding up DataFrame operations where possible

In these utilities we use Dask where it's installed and enabled (and return Pandas results), or
else default to Pandas operations.

Some best practices:

- This module's `suggest_num_dask_partitions()` suggest an appropriate number of Dask partitions
- Make sure reset_index is only done in Pandas and not Dask, as mentioned at:
  https://docs.dask.org/en/latest/dataframe-best-practices.html
- See also https://docs.dask.org/en/latest/best-practices.html

While Dask already offers APIs very close to Pandas, the aim of this utility is for the notebook to
(as far as possible) not have to worry about whether the calculation is running in plain Pandas or
not.

We also explored Ray through the Modin library, but found an error (below) when adding a new column
to Modin dataframes. Perhaps this issue will be solved in future:

https://github.com/modin-project/modin/issues/2442
"""

# Python Built-Ins:
from typing import Callable, Iterable, List, Tuple, Union
import warnings

# External Dependencies:
try:
    import dask
    import dask.dataframe as dd
    from dask.diagnostics import ProgressBar
    HAS_DASK = True
except ImportError:
    warnings.warn("dask[dataframe] not installed: Using pure pandas")
    HAS_DASK = False
import pandas as pd


def suggest_num_dask_partitions(forecast_dimensions: List[str], num_items: int) -> int:
    """Suggest a likely appropriate npartitions for Dask based on Forecast problem attributes

    As a best practice, we suggest using 1 partition if item_id is the only dimension in the
    dataset, or otherwise using num_items.

    See more information at: https://docs.dask.org/en/latest/best-practices.html

    Arguments
    ---------
    forecast_dimensions : List[str]
        List of dimensions (column names) in the target time-series excluding the timestamp and the
        target value itself. E.g. ["item_id"] or ["item_id", "location"].
    num_items : int
        Number of unique item IDs in the dataset ()
    left : pd.DataFrame
        Left DataFrame for the join
    right : pd.DataFrame
        Right DataFrame for the join
    num_dask_partitions : int
        As a best practice, consider choosing paritions to be number of items if your timeseries
        has more dimensions than just item_id, or just leave default otherwise. Default 1. See:
        https://docs.dask.org/en/latest/best-practices.html
    use_dask_if_available : bool
        Set `False` to disable distributing the computation with Dask, even if Dask is installed.
        Default True
    **merge_kwargs :
        Passed through to Pandas `merge()` or Dask `merge()` as appropriate
    """
    return 1 if len(forecast_dimensions) > 1 else num_items

    
def group_and_apply(
    df: pd.DataFrame,
    group_by_cols: Iterable[str],
    apply_fn: Callable,
    output_meta: Union[pd.DataFrame, pd.Series, dict, Iterable, Tuple],
    num_dask_partitions: int=1,
    use_dask_if_available: bool=True,
) -> pd.DataFrame:
    """Group df by `group_by_cols` and apply function `apply_fn` to the grouped frames

    Arguments
    ---------
    df : pd.DataFrame
        Dataframe to be processed
    group_by_cols : Iterable[str]
        List of column names to group the dataframe by
    apply_fn : Callable
        Function to `.apply(...)` to process each group.
    output_meta: Union[pd.DataFrame, pd.Series, dict, Iterable, Tuple]
        An empty DataFrame or Series that hints the dtypes and column names of the output. Required
        if dask is used, otherwise ignored.
    num_dask_partitions : int
        See `suggest_num_dask_partitions()` in this module for guidance on setting this. Ignored
        if dask is not used.
    use_dask_if_available : bool
        Set `False` to disable distributing the computation with Dask, even if Dask is installed.
        Default True

    Returns
    -------
    result : pd.DataFrame
        Equivalent result of df.groupby().apply() in Pandas
    """
    if HAS_DASK and use_dask_if_available:
        print("Aggregating with Dask")
        ddf = dd.from_pandas(df, num_partitions)
        return ddf.groupby(group_by_cols).apply(apply_fn, meta=output_meta).compute()
    else:
        print("Aggregating with Pandas")
        return df.groupby(group_by_cols).apply(apply_fn)


def merge(
    left: pd.DataFrame,
    right: pd.DataFrame,
    num_dask_partitions: int=1,
    use_dask_if_available: bool=True,
    **merge_kwargs,
):
    """Perform a DataFrame `merge` (join) operation

    Arguments
    ---------
    left : pd.DataFrame
        Left DataFrame for the join
    right : pd.DataFrame
        Right DataFrame for the join
    num_dask_partitions : int
        See `suggest_num_dask_partitions()` in this module for guidance on setting this. Ignored
        if dask is not used.
    use_dask_if_available : bool
        Set `False` to disable distributing the computation with Dask, even if Dask is installed.
        Default True
    **merge_kwargs :
        Passed through to Pandas `merge()` or Dask `merge()` as appropriate

    Returns
    -------
    result : pd.DataFrame
        Merged result
    """
    if HAS_DASK and use_dask_if_available:
        print("Merging DataFrames L={}, R={} with Dask (npartitions={})".format(
            left.shape,
            right.shape,
            num_dask_partitions,
        ))
        ddf = dd.from_pandas(left, npartitions=num_dask_partitions)
        return ddf.merge(right, **merge_kwargs).compute()
    else:
        print("Merging DataFrames L={}, R={} in plain Pandas".format(
            left.shape,
            right.shape,
        ))
        return left.merge(right, **merge_kwargs)
