"""Visualization and plotting utilities for Amazon Forecast pre-PoC workshop
"""

# Python Built-Ins:
from typing import Optional

# External Dependencies:
from matplotlib import pyplot as plt
import pandas as pd

# Local Dependencies
from .dataprep import select_by_df


def configure_pandas_display():
    """Make pandas previews display nicely in the notebook
    """
    # Display all columns wide:
    pd.set_option("display.max_columns", None)
    # Display horizontal scrollbar for wide columns:
    pd.set_option("display.width", 5000)
    pd.set_option("display.max_colwidth", 5000)
    # Display all rows:
    pd.set_option("display.max_rows", 1000)
    # Turn off scientific notation:
    pd.set_option("display.float_format", lambda x: "%.5f" % x)


def make_plots(
    df: pd.DataFrame,
    sample_series: pd.DataFrame,
    target_value_col: str,
    y_axis_label: Optional[str]=None,
) -> None:
    """Plot a subset of the timeseries in the dataframe

    Arguments
    ---------
    df : pd.DataFrame
        Frame of the full timeseries data
    sample_series : pd.DataFrame
        Frame of filtering criteria to be plotted: `len(sample_series)` plots will be produced, and
        columns should be a subset of `df`.
    target_value_col : str
        Name of the column of `df` containing the actual value of the time-series to be plotted.
    y_axis_label : Optional[str]
        Optional label to be added to the Y axis
    """
    num_plots = len(sample_series)
    if num_plots > 20:
        # Avoid crashing / weird errors if the input looks like an error
        raise ValueError(
            "Producing {} plots on one figure likely a mistake: Check sample_series".format(
                num_plots
            )
        )

    # resize plots smaller if fewer time series to plot
    if num_plots >= 5:
        fig, axs = plt.subplots(num_plots, 1, figsize=(15, 15), sharex=True)
    elif num_plots > 1:
        fig, axs = plt.subplots(num_plots, 1, figsize=(15, 8), sharex=True)
    else:
        # default at least 2 plots otherwise axs indexing breaks
        fig, axs = plt.subplots(2, 1, figsize=(15, 8), sharex=True)
    # fig.subplots_adjust(hspace=0.5) # pad a little if each x-axis has title

    # set a global y-axis label
    fig.text(0.04, 0.5, y_axis_label, va="center", rotation="vertical")

    plots_missing_data = []
    for i in range(num_plots):
        ax = axs[i]
        series_descriptor = sample_series.iloc[i]  # column-keyed pd.Series describing this plot
        zoomed = select_by_df(df, sample_series.iloc[i:i+1])  # This subset of df

        ax.grid(False)

        # plot only if time series exists
        if not (zoomed.shape[0] > 0):
            plots_missing_data.append(i)  # We'll add a label below
        else:
            zoomed[[target_value_col]].plot(ax=ax)
            # remove auto-generated subplot legend
            ax.get_legend().remove()
            ax.grid(which="major", axis="x")

        ax.set_title(
            # e.g. "item_id 341, location abc-def"
            ", ".join([f"{k} {v}" for k, v in series_descriptor.iteritems()])
        )

        # format the x-axis
        ax.set_xlabel("Timestamp")  # set x-axis title
        ax.xaxis.label.set_visible(False)

    # Add centered warnings/info to all the plots where no data was found:
    for ax in map(lambda i: axs[i], plots_missing_data):
        xlims = ax.get_xlim()
        ylims = ax.get_ylim()
        axs[i].text(
            (xlims[0] + xlims[1]) / 2,
            (ylims[0] + ylims[1]) / 2,
            "No data available",
            ha="center",
        )

    plt.plot()
