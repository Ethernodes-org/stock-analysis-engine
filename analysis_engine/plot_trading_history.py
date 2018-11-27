"""
Plot a ``Trading History`` dataset using seaborn and matplotlib
"""

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import analysis_engine.consts as ae_consts
import analysis_engine.charts as ae_charts
import analysis_engine.build_result as build_result
import spylunking.log.setup_logging as log_utils

log = log_utils.build_colorized_logger(name=__name__)


def plot_trading_history(
        title,
        df,
        red,
        red_color=None,
        blue=None,
        blue_color=None,
        green=None,
        green_color=None,
        orange=None,
        orange_color=None,
        date_col='date',
        xlabel='Date',
        ylabel='Algo Values',
        linestyle='-',
        width=8.0,
        height=6.0,
        date_format='%d\n%b',
        df_filter=None,
        start_date=None,
        footnote_text=None,
        footnote_xpos=0.70,
        footnote_ypos=0.01,
        footnote_color='#888888',
        footnote_fontsize=8,
        scale_y=False,
        show_plot=True,
        dropna_for_all=False,
        verbose=False):
    """plot_trading_history

    Plot columns up to 4 lines from the ``Trading History`` dataset

    :param title: title of the plot
    :param df: dataset which is ``pandas.DataFrame``
    :param red: string - column name to plot in
        ``red_color`` (or default ``ae_consts.PLOT_COLORS[red]``)
        where the column is in the ``df`` and
        accessible with:``df[red]``
    :param red_color: hex color code to plot the data in the
        ``df[red]``  (default is ``ae_consts.PLOT_COLORS[red]``)
    :param blue: string - column name to plot in
        ``blue_color`` (or default ``ae_consts.PLOT_COLORS[blue]``)
        where the column is in the ``df`` and
        accessible with:``df[blue]``
    :param blue_color: hex color code to plot the data in the
        ``df[blue]``  (default is ``ae_consts.PLOT_COLORS[blue]``)
    :param green: string - column name to plot in
        ``green_color`` (or default ``ae_consts.PLOT_COLORS[green]``)
        where the column is in the ``df`` and
        accessible with:``df[green]``
    :param green_color: hex color code to plot the data in the
        ``df[green]``  (default is ``ae_consts.PLOT_COLORS[green]``)
    :param orange: string - column name to plot in
        ``orange_color`` (or default ``ae_consts.PLOT_COLORS[orange]``)
        where the column is in the ``df`` and
        accessible with:``df[orange]``
    :param orange_color: hex color code to plot the data in the
        ``df[orange]``  (default is ``ae_consts.PLOT_COLORS[orange]``)
    :param date_col: string - date column name
        (default is ``date``)
    :param xlabel: x-axis label
    :param ylabel: y-axis label
    :param linestyle: style of the plot line
    :param width: float - width of the image
    :param height: float - height of the image
    :param date_format: string - format for dates
    :param df_filter: optional - initialized ``pandas.DataFrame`` query
        for reducing the ``df`` records before plotting. As an eaxmple
        ``df_filter=(df['close'] > 0.01)`` would find only records in
        the ``df`` with a ``close`` value greater than ``0.01``
    :param start_date: optional - string ``datetime``
        for plotting only from a date formatted as
        ``YYYY-MM-DD HH\:MM\:SS``
    :param footnote_text: optional - string footnote text
        (default is ``algotraders <DATE>``)
    :param footnote_xpos: optional - float for footnote position
        on the x-axies
        (default is ``0.75``)
    :param footnote_ypos: optional - float for footnote position
        on the y-axies
        (default is ``0.01``)
    :param footnote_color: optional - string hex color code for
        the footnote text
        (default is ``#888888``)
    :param footnote_fontsize: optional - float footnote font size
        (default is ``8``)
    :param scale_y: optional - bool to scale the y-axis with
        .. code-block:: python

            use_ax.set_ylim(
                [0, use_ax.get_ylim()[1] * 3])
    :param show_plot: bool to show the plot
    :param dropna_for_all: optional - bool to toggle keep None's in
        the plot ``df`` (default is drop them for display purposes)
    :param verbose: optional - bool to show logs for debugging
        a dataset
    """

    rec = {
        'ax1': None,
        'ax2': None,
        'ax3': None,
        'ax4': None,
        'fig': None
    }
    result = build_result.build_result(
        status=ae_consts.NOT_RUN,
        err=None,
        rec=rec)

    if verbose:
        log.info('plot_trading_history - start')

    use_red = red_color
    use_blue = blue_color
    use_green = green_color
    use_orange = orange_color

    if not use_red:
        use_red = ae_consts.PLOT_COLORS['red']
    if not use_blue:
        use_blue = ae_consts.PLOT_COLORS['blue']
    if not use_green:
        use_green = ae_consts.PLOT_COLORS['green']
    if not use_orange:
        use_orange = ae_consts.PLOT_COLORS['orange']

    use_footnote = footnote_text
    if not use_footnote:
        use_footnote = (
            'algotraders - {}'.format(
                datetime.datetime.now().strftime(
                    ae_consts.COMMON_TICK_DATE_FORMAT)))

    column_list = [
        date_col
    ]
    all_plots = []
    if red:
        column_list.append(red)
        all_plots.append({
            'column': red,
            'color': use_red})
    if blue:
        column_list.append(blue)
        all_plots.append({
            'column': blue,
            'color': use_blue})
    if green:
        column_list.append(green)
        all_plots.append({
            'column': green,
            'color': use_green})
    if orange:
        column_list.append(orange)
        all_plots.append({
            'column': orange,
            'color': use_orange})

    use_df = df
    if start_date:
        start_date_value = datetime.datetime.strptime(
            start_date,
            ae_consts.COMMON_TICK_DATE_FORMAT)
        use_df = df[(df[date_col] >= start_date_value)][column_list]
    # end of filtering by start date

    if verbose:
        log.info(
            'plot_history_df start_date={} df.index={} column_list={}'.format(
                start_date,
                len(use_df.index),
                column_list))

    if hasattr(df_filter, 'to_json'):
        use_df = use_df[df_filter][column_list]

    if verbose:
        log.info(
            'plot_history_df filter df.index={} column_list={}'.format(
                start_date,
                len(use_df.index),
                column_list))

    if dropna_for_all:
        use_df = use_df.dropna(axis=0, how='any')
        if verbose:
            log.info('plot_history_df dropna_for_all')
    # end of pre-plot dataframe scrubbing

    ae_charts.set_common_seaborn_fonts()

    hex_color = ae_consts.PLOT_COLORS['blue']
    fig, ax = plt.subplots(
        sharex=True,
        sharey=True,
        figsize=(
            width,
            height))

    all_axes = []
    num_plots = len(all_plots)
    for idx, node in enumerate(all_plots):
        column_name = node['column']
        hex_color = node['color']

        use_ax = ax
        if idx > 0:
            use_ax = ax.twinx()

        if verbose:
            log.info(
                'plot_history_df - {}/{} - {} in {} - ax={}'.format(
                    (idx + 1),
                    num_plots,
                    column_name,
                    hex_color,
                    use_ax))

        all_axes.append(use_ax)
        if linestyle == '-':
            use_df[[date_col, column_name]].plot(
                x=date_col,
                linestyle=linestyle,
                ax=use_ax,
                color=hex_color,
                rot=0)
        else:
            use_df[[date_col, column_name]].plot(
                kind='bar',
                x=date_col,
                ax=use_ax,
                color=hex_color,
                rot=0)

        if idx > 0:
            if scale_y:
                use_ax.set_ylim(
                    [0, use_ax.get_ylim()[1] * 3])
            use_ax.fmt_xdata = mdates.DateFormatter(date_format)
            use_ax.xaxis.grid(False)
            use_ax.yaxis.grid(False)
            use_ax.yaxis.set_ticklabels([])
        else:
            use_ax.xaxis.grid(
                True,
                which='minor')
            use_ax.fmt_xdata = mdates.DateFormatter(
                date_format)
            use_ax.xaxis.set_minor_formatter(
                use_ax.fmt_xdata)
            plt.grid(True)
    # end of for all plots

    handles, labels = plt.gca().get_legend_handles_labels()
    newLabels, newHandles = [], []
    for handle, label in zip(handles, labels):
        if label not in newLabels:
            newLabels.append(label)
            newHandles.append(handle)

    lines = []
    for idx, cur_ax in enumerate(all_axes):
        lines += cur_ax.get_lines()
        rec['ax{}'.format(idx + 1)] = use_ax
    # Build out the xtick chart by the dates

    # turn off the grids on volume

    ax.legend(
        lines,
        [l.get_label() for l in lines],
        loc='best',
        shadow=True)

    fig.autofmt_xdate()

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    ax.set_title(title)
    ae_charts.add_footnote(
        fig=fig,
        xpos=footnote_xpos,
        ypos=footnote_ypos,
        text=use_footnote,
        color=footnote_color,
        fontsize=footnote_fontsize)
    plt.tight_layout()

    plt.show()
    if show_plot:
        plt.show()
    else:
        plt.plot()

    rec['fig'] = fig

    result = build_result.build_result(
        status=ae_consts.SUCCESS,
        err=None,
        rec=rec)

    return result
# end of plot_history_df
