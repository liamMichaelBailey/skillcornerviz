"""
Liam Bailey
Last update MN 20/04/2023
Added _rev function ; Changed initial function

Markos Bontozoglou
12/06/2024
Summary Table
The plot_summary_table function is used to generate a summary table based on the given data.
It accepts various parameters such as the DataFrame (df) containing the metric data,
the names that are given to each column (metric_col_names), the size of the summary table (fig_size),
the metadata columns to include in the summary table (meta), and the format which the summary table will
be presented in (mode).
"""
import matplotlib.pyplot as plt
# ----------------
# PLOT REGULAR TABLE WITH PLAYERS AS ROWS : BEST IF YOU HAVE A LOT OF PLAYERS
# ----------------
from matplotlib.patches import Rectangle
from skillcornerviz.utils.constants import GREEN_TO_RED_SCALE, DARK_GREEN_TO_RED_SCALE, \
    DARK_PRIMARY_HIGHLIGHT_COLOR
from skillcornerviz.utils.constants import TEXT_COLOR, DARK_BASE_COLOR
from skillcornerviz.utils import skillcorner_utils as skcu
from pkg_resources import resource_filename
from matplotlib import font_manager as fm

fonts = ['resources/Roboto/Roboto-Black.ttf',
         'resources/Roboto/Roboto-BlackItalic.ttf',
         'resources/Roboto/Roboto-Bold.ttf',
         'resources/Roboto/Roboto-BoldItalic.ttf',
         'resources/Roboto/Roboto-Italic.ttf',
         'resources/Roboto/Roboto-Light.ttf',
         'resources/Roboto/Roboto-LightItalic.ttf',
         'resources/Roboto/Roboto-Medium.ttf',
         'resources/Roboto/Roboto-MediumItalic.ttf',
         'resources/Roboto/Roboto-Regular.ttf',
         'resources/Roboto/Roboto-Thin.ttf',
         'resources/Roboto/Roboto-ThinItalic.ttf']

for f in fonts:
    filepath = resource_filename('skillcornerviz', f)
    fm.fontManager.addfont(filepath)
plt.rcParams["font.family"] = "Roboto"


def plot_summary_table(df,
                       metrics,
                       metric_col_names,
                       players,
                       figsize=(10, 4),
                       meta=['player_name'],
                       mode='value+rank'):
    """
    Plot a summary table with players as rows.

    Parameters:
    - df (DataFrame): The data to be visualized in the table.
    - metrics (list): List of metric names to display.
    - metric_col_names (list): List of column names for metrics.
    - players (list): List of player names to include in the table.
    - figsize (tuple): Figure size (width, height).
    - meta (list): List of metadata columns.
    - mode (str): Display mode ('value+rank', 'rank', 'value').

    Returns:
    - fig (Figure): The Matplotlib Figure object.
    - ax (Axes): The Matplotlib Axes object.
    """
    plot_df = df[df['player_name'].isin(players)]
    # Filters the DataFrame to only include rows that include 'player_name' in the list 'players'
    plot_df = plot_df.iloc[::-1]
    # Reverses the order of the rows in the DataFrame
    plot_df = plot_df.reset_index(drop=True)
    # Resets the indexes of the DataFrame

    fig, ax = plt.subplots(figsize=figsize)  # Creates a figure

    # Initialize metric columns and their rank columns with a default rank of 'Very Low'
    for m in metrics:
        plot_df[m] = plot_df[m].round(1)
        plot_df[m + '_rank'] = 'Very Low'

    # Assign ranks based on the standard deviation bins
    pct_bins = [-2, -1, 1, 2]
    bin_names = ['Low', 'Average', 'High', 'Very High']
    for bin, name in zip(pct_bins, bin_names):
        for m in metrics:
            plot_df.loc[plot_df[m] > df[m].mean() +
                        (df[m].std() * bin),
                        m + '_rank'] = name

    columns = meta.copy()
    columns += metrics

    # Formatting of column names
    column_names = [i.replace('_', ' ').title().replace(' ', '\n') for i in meta]

    column_names += metric_col_names

    # Determine positions for the columns in the summary table
    if len(meta) == 1:
        positions = [0.25]
    else:
        positions = [0.25 + 2 * i for i in range(len(meta))]

    # Add the positions for the columns
    i = max(positions) + 1.75
    for m in metrics:
        positions.append(i)
        i += 1.25

    n_rows = plot_df.shape[0]

    # Sets limits for x, y axes
    ax.set_xlim(0, max(positions) + 0.5)
    ax.set_ylim(0, n_rows + 1)

    # Add table's main text
    for i in range(n_rows):
        for j, column in enumerate(columns):
            if j == 0:
                ha = 'left'
            else:
                ha = 'center'

            if 'ratio' in column.lower() or 'percentage' in column.lower():
                appendix = ' %'
            else:
                appendix = ''

            if column in meta:
                text_label = f'{plot_df[column].iloc[i]}'
                text_label = "\n".join(text_label.split(" ", 1))
                rank_label = ''
                weight = 'bold'
                annotation_text = text_label + appendix + rank_label
            else:
                text_label = f'{plot_df[column].iloc[i]}'
                rank_label = f'{plot_df[column + "_rank"].iloc[i]}'
                rank_label = '\n' + rank_label
                weight = 'normal'
                if mode == 'value+rank':
                    annotation_text = text_label + appendix + rank_label
                elif mode == 'rank':
                    annotation_text = rank_label.replace('\n', '')
                elif mode == 'value':
                    annotation_text = text_label + appendix

            if 'High' in rank_label:
                colour = GREEN_TO_RED_SCALE[4]
                weight = 'bold'
            elif 'Low' in rank_label:
                colour = GREEN_TO_RED_SCALE[0]
                weight = 'bold'
            else:
                colour = TEXT_COLOR

            ax.annotate(
                xy=(positions[j], i + .5),
                text=annotation_text,
                ha=ha,
                va='center',
                weight=weight,
                color=colour
            )

    # Add column names
    for index, c in enumerate(column_names):
        if index == 0:
            ha = 'left'
        else:
            ha = 'center'

        if len(c) > 25:
            column_label = skcu.split_string_with_new_line(c)
        else:
            column_label = c

        ax.annotate(
            xy=(positions[index], n_rows + .25),
            text=column_label,
            ha=ha,
            va='bottom',
            weight='bold',
            color=TEXT_COLOR
        )

    # Add dividing lines
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [n_rows, n_rows], lw=1.5, color=TEXT_COLOR, marker='', zorder=4)
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=1.5, color=TEXT_COLOR, marker='', zorder=4)
    for x in range(1, n_rows):
        ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x, x], lw=1.15, color=TEXT_COLOR, alpha=0.5, ls=':', zorder=3,
                marker='')

    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

    return fig, ax


# ----------------
# PLOT TABLE WITH PLAYERS AS COLUMNS : BEST IF YOU HAVE A LOT OF METRICS
# ----------------


def plot_summary_table_rev(df, metrics, metric_col_names, players, figsize=(10, 4), meta=None,
                           mode='values+rank',
                           percentiles_mode=False,
                           font_size=None,
                           dividing_lines=None,
                           metric_col_space=None,
                           data_point_id='player_name',
                           data_point_label='player_name',
                           column_order=None,
                           split_column_names=True,
                           dark_mode=False,
                           rotate_column_names=False,
                           split_metric_names=True):
    """
    Plot a summary table with players as columns.

    Parameters:
    - df (DataFrame): The data to be visualized in the table.
    - metrics (list): List of metric names to display.
    - metric_col_names (list): List of column names for metrics.
    - players (list): List of player names to include in the table.
    - figsize (tuple): Figure size (width, height).
    - meta (list): List of metadata columns.
    - mode (str): Display mode ('values+rank', 'rank', 'values').
    - percentiles_mode (bool): Whether to use percentiles for ranking.
    - font_size (float): Font size for the table.
    - dividing_lines (list): Positions to add dividing lines.
    - metric_col_space (float): Space between metric columns.
    - data_point_id (str): The data point identifier column.
    - data_point_label (str): The label for data points.
    - column_order (list): Custom order of player columns.
    - split_column_names (bool): Split long column names.
    - dark_mode (bool): Enable dark mode (True) or light mode (False).
    - rotate_column_names (bool): Rotate column names if True.
    - split_metric_names (bool): Split long metric names.

    Returns:
    - fig (Figure): The Matplotlib Figure object.
    - ax (Axes): The Matplotlib Axes object.
    """

    # Assinging values to parameters if none are given
    if dividing_lines is None:
        dividing_lines = []
    if meta is None:
        meta = [data_point_id]

    if font_size is None:
        if len(players) <= 9:
            font_size = 9
        elif len(players) <= 12:
            font_size = 7
        else:
            font_size = 6.5

    # Assigning a space between metric columns if there is none given.
    if metric_col_space is None:
        if len(players) <= 4:
            metric_col_space = 1.5
        elif len(players) <= 7:
            metric_col_space = 2.5
        elif len(players) <= 14:
            metric_col_space = 3
        else:
            metric_col_space = 3.5

    # Split column names if they are too long.
    if split_metric_names:
        metric_col_names = [skcu.split_string_with_new_line(s) if len(s) > 25 else s for s in metric_col_names]

    plot_df = df.copy()

    # Rounds each metric to one decimal place
    for m in metrics:
        plot_df[m] = plot_df[m].round(1)

    if not percentiles_mode:
        pct_bins = [0, 10, 20, 80, 90]
        bin_names = ['Very Low', 'Low', 'Average', 'High', 'Very High']
        for bin, name in zip(pct_bins, bin_names):
            for m in metrics:
                plot_df.loc[(plot_df[m].rank(pct=True, na_option='keep') * 100).round(2) >= int(bin),
                            m + '_pct'] = name
    else:
        skcu.add_percentile_values(plot_df, metrics)

    # Filters the df to only include players that are in the list 'players'
    plot_df = plot_df[plot_df[data_point_id].isin(players)]

    # Will have two lists, one with the player ID's, and one with their names
    players = list(plot_df[data_point_id])
    player_names = list(plot_df[data_point_label])

    text_color = 'white' if dark_mode else TEXT_COLOR
    facecolor = TEXT_COLOR if dark_mode else 'white'

    red_highlight = DARK_GREEN_TO_RED_SCALE[1] if dark_mode else GREEN_TO_RED_SCALE[0]
    green_highlight = DARK_GREEN_TO_RED_SCALE[3] if dark_mode else GREEN_TO_RED_SCALE[4]

    # Plot setup.
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(facecolor)
    ax.set_facecolor(facecolor)

    # DIFFERENCE with previous plot
    # Formatting of the DataFrame
    for i in metrics:
        plot_df[i] = plot_df[i].astype(str) + ' ' + plot_df[i + '_pct'].astype(str)
    plot_df = plot_df[meta + metrics]
    meta_names = [i.replace('_', ' ').capitalize() for i in meta]
    plot_df.columns = meta_names + metric_col_names

    plot_df = plot_df.set_index(data_point_id.replace('_', ' ').capitalize()).T.reset_index()
    plot_df = plot_df.iloc[::-1].reset_index(drop=True)

    if column_order is None:
        # Columns start with index and then are followed by player ID's
        columns = ['index'] + players
        if split_column_names is True:
            # Splits columns using a newline character
            column_names = [''] + [skcu.split_string_with_new_line(i) for i in player_names]
        else:
            column_names = [''] + player_names
    else:
        # If a custom column order is given, columns are assigned this order
        columns = ['index'] + column_order
        if split_column_names is True:
            # Splits columns using a newline character
            column_names = [''] + [skcu.split_string_with_new_line(i) for i in column_order]
        else:
            column_names = [''] + column_order

    positions = [0.0] + [(i + metric_col_space) * 2 for i in range(0, len(players))]
    n_rows = plot_df.shape[0]

    ax.set_xlim(0, max(positions) + 1)
    ax.set_ylim(0, n_rows + 1)

    # Add table's main text
    for i in range(n_rows):
        for j, column in enumerate(columns):
            if j == 0:
                ha = 'left'
            else:
                ha = 'center'

            if j != 0:
                if 'ratio ' in ' ' + plot_df['index'].iloc[i].lower() + ' ' or \
                        ' percentage ' in ' ' + plot_df['index'].iloc[i].lower() + ' ' or \
                        ' % ' in ' ' + plot_df['index'].iloc[i].lower() + ' ' or \
                        ' ratio' in ' ' + plot_df['index'].iloc[i].lower():
                    appendix = ' %'
                elif ' velocity ' in ' ' + plot_df['index'].iloc[i].lower() + ' ' or \
                        ' psv-99 ' in ' ' + plot_df['index'].iloc[i].lower() + ' ':
                    appendix = ' km/h'
                elif ' distance ' in ' ' + plot_df['index'].iloc[i].lower() + ' ':
                    appendix = 'm'
                elif ' meters per minute ' in ' ' + plot_df['index'].iloc[i].lower() + ' ':
                    appendix = 'm'
                elif ' threat ' in ' ' + plot_df['index'].iloc[i].lower() + ' ':
                    appendix = ''
                elif ' passes ' in ' ' + plot_df['index'].iloc[i].lower() + ' ' or \
                        ' pass ' in ' ' + plot_df['index'].iloc[i].lower() + ' ':
                    appendix = ' Passes'
                elif ' runs ' in ' ' + plot_df['index'].iloc[i].lower() + ' ':
                    appendix = ' Runs'
                else:
                    appendix = ''
            else:
                appendix = ''

            if column == 'index':
                text_label = f'{plot_df[column].iloc[i]}'
                rank_label = ''
                weight = 'bold'
                annotation_text = text_label + appendix + rank_label
            elif plot_df['index'][i] in meta_names:
                text_label = f'{plot_df[column].iloc[i]}'
                if len(text_label.split(' ')) > 1:
                    text_label = skcu.split_string_with_new_line(text_label)
                weight = 'normal'
                annotation_text = text_label
                rank_label = ''
            else:
                text_label = f'{plot_df[column].iloc[i]}'

                split_text_label = text_label.split(" ", 1)

                text_label = split_text_label[0]
                rank_label = split_text_label[1].split('.')[0]

                weight = 'normal'
                if mode == 'values+rank':
                    annotation_text = text_label + appendix + '\n' + rank_label
                elif mode == 'rank':
                    annotation_text = rank_label
                elif mode == 'values':
                    annotation_text = text_label + appendix
                else:
                    annotation_text = ''

            if 'nan' not in str(plot_df[column].iloc[i]):
                if not percentiles_mode or column == 'index':
                    if 'High' in rank_label:
                        colour = green_highlight
                        weight = 'bold'
                    elif 'Low' in rank_label:
                        colour = red_highlight
                        weight = 'bold'
                    else:
                        colour = text_color
                elif percentiles_mode:
                    if rank_label != '':
                        if float(rank_label) > 79:
                            colour = green_highlight
                            weight = 'bold'
                            bar_color = colour
                        elif float(rank_label) < 21:
                            colour = red_highlight
                            weight = 'bold'
                            bar_color = colour
                        else:
                            colour = text_color
                            bar_color = DARK_BASE_COLOR
                    else:
                        colour = text_color
                        bar_color = DARK_BASE_COLOR

                    if mode != 'values':  ### HUMANIZE PACKAGE
                        if rank_label != '':
                            if rank_label[-1] == '3':
                                annotation_text = annotation_text + 'rd'
                            elif rank_label[-1] == '1':
                                annotation_text = annotation_text + 'st'
                            elif rank_label[-1] == '2':
                                annotation_text = annotation_text + 'nd'
                            else:
                                annotation_text = annotation_text + 'th'

                    if column != 'index':
                        if rank_label != '':
                            ax.add_patch(
                                Rectangle((positions[j] - 1, i), 2 * float(rank_label) / 100, 1, fc=bar_color,
                                          edgecolor=DARK_BASE_COLOR if dark_mode else 'black',
                                          alpha=0.5 if dark_mode else 0.1))
                else:
                    colour = TEXT_COLOR

                ax.annotate(
                    xy=(positions[j], i + .5),
                    text=annotation_text,
                    ha=ha,
                    va='center',
                    weight=weight,
                    color=colour,
                    font_size=font_size,
                    zorder=10
                )
            else:
                ax.annotate(
                    xy=(positions[j], i + .5),
                    text='No Data',
                    ha=ha,
                    va='center',
                    weight=weight,
                    color=TEXT_COLOR,
                    font_size=font_size,
                    zorder=10)

                if percentiles_mode:
                    ax.add_patch(
                        Rectangle((positions[j] - 1, i), 2 * float(100) / 100, 1, fc='white',
                                  edgecolor=DARK_BASE_COLOR if dark_mode else 'black',
                                  alpha=0.5 if dark_mode else 0.1))

    # Add column names
    for index, c in enumerate(column_names):
        if index == 0:
            ha = 'left'
        else:
            ha = 'center'

        if rotate_column_names:
            rotation = 30
        else:
            rotation = 0
        ax.annotate(
            xy=(positions[index], n_rows + .25),
            text=column_names[index],
            ha=ha,
            va='bottom',
            weight='bold',
            color=text_color,
            font_size=font_size,
            rotation=rotation
        )

    # Add dividing lines
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [n_rows, n_rows], lw=1.5,
            color=DARK_PRIMARY_HIGHLIGHT_COLOR if dark_mode else text_color, marker='', zorder=4)
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=1.5,
            color=DARK_PRIMARY_HIGHLIGHT_COLOR if dark_mode else text_color, marker='', zorder=4)

    for i in dividing_lines:
        ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [i, i], lw=1.5, color=DARK_BASE_COLOR, marker='', zorder=4)

    for x in range(1, n_rows):
        ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x, x], lw=.5, color=DARK_BASE_COLOR, alpha=0.5, ls='-',
                zorder=3,
                marker='')

    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

    return fig, ax
