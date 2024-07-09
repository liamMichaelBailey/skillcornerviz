"""
Liam Bailey
09/03/2023
SkillCorner Swarm & Violin Plots.
This code defines a function `plot_swarm_violin` that plots a swarm/violin plot
using the seaborn and matplotlib libraries. The function takes several parameters
including the DataFrame (`df`), the columns to plot on the x-axis (`x_metric`)
and y-axis (`y_metric`), the categorical values to include on the y-axis
(`y_groups`), and other optional parameters such as labels, colors, and
highlighting specific data points.
"""
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from adjustText import adjust_text
import seaborn as sns
from matplotlib.ticker import EngFormatter
from skillcornerviz.utils.constants import BASE_COLOR, PRIMARY_HIGHLIGHT_COLOR, SECONDARY_HIGHLIGHT_COLOR
from skillcornerviz.utils.constants import TEXT_COLOR
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


def plot_swarm_violin(df,
                      x_metric,
                      y_metric,
                      y_groups=None,
                      x_label=None,
                      y_group_labels=None,
                      x_unit=None,
                      primary_highlight_group=None,
                      secondary_highlight_group=None,
                      data_point_id='player_name',
                      data_point_label='player_name',
                      label_fontsize=7,
                      fontsize=7,
                      point_size=9,
                      highlight_point_size=10,
                      base_colour=BASE_COLOR,
                      primary_highlight_color=PRIMARY_HIGHLIGHT_COLOR,
                      secondary_highlight_color=SECONDARY_HIGHLIGHT_COLOR,
                      figsize=(8, 4)):
    """
    Plots a swarm/violin plot.

    Parameters:
    -----------
    df : DataFrame
        Metric DataFrame.
    x_metric : str
        The column in df we want to plot on the x-axis.
    y_metric : str
        The column in df we want to plot on the y-axis. This should be categorical.
    y_groups : list[str], optional
        The categorical values from the y_value column we want to include.
    x_label : str, optional
        The label for the x-axis. This should reflect what the x_value is.
    y_group_labels : list[str], optional
        The labels for the y-axis. This should reflect the data being split across the y-axis.
    x_unit : str, optional
        If we want to add a unit to the axis values. For example % or km/h.
    secondary_highlight_group : list, optional
        A group of players to label & highlight in SkillCorner yellow.
    primary_highlight_group : list, optional
        A group of players to label & highlight in SkillCorner red.
    data_point_id : str, optional
        The column in df that represents the unique identifier for each data point.
    data_point_label : str, optional
        The column in df that contains the labels to display for each data point.
    base_colour : str, optional
        The base color for the plot.
    primary_highlight_color : str, optional
        The highlight color for the primary highlight group.
    secondary_highlight_color : str, optional
        The highlight color for the secondary highlight group.
    figsize : tuple, optional
        The size of the figure (width, height).

    Returns:
    --------
    fig : Figure
        The generated figure.
    ax : Axes
        The axes of the generated plot.
    """

    # Adding values to parameters that were not given a value
    if y_groups is None:
        y_groups = list(df[y_metric].unique())

    if x_label is None:
        x_label = x_metric

    if y_group_labels is None:
        y_group_labels = y_groups

    if primary_highlight_group is None:
        primary_highlight_group = []

    if secondary_highlight_group is None:
        secondary_highlight_group = []

    # Removing unseemly categories in the y_value column.
    plot_data = df[df[y_metric].isin(y_groups)]

    # Setting size & face colors.
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # Plotting violins.
    violin_parts = sns.violinplot(data=plot_data,
                                  x=x_metric,
                                  y=y_metric,
                                  order=y_groups,
                                  inner=None,
                                  width=1,
                                  zorder=5)

    # Setting the style for each violin.
    for pc in violin_parts.collections:
        pc.set_facecolor(TEXT_COLOR)
        pc.set_edgecolor(TEXT_COLOR)
        pc.set_linewidth(0.5)
        pc.set_alpha(0.075)

    # Setting swarm groups: background_players, comparison_players, target_player.
    plot_data = plot_data.assign(swarm_group='background_group')
    plot_data = plot_data.assign(colour=base_colour)

    plot_data.loc[plot_data[data_point_id].isin(primary_highlight_group), 'swarm_group'] = 'primary_highlight_group'
    plot_data.loc[plot_data[data_point_id].isin(primary_highlight_group), 'colour'] = primary_highlight_color

    plot_data.loc[plot_data[data_point_id].isin(secondary_highlight_group), 'swarm_group'] = 'secondary_highlight_group'
    plot_data.loc[plot_data[data_point_id].isin(secondary_highlight_group), 'colour'] = secondary_highlight_color

    sns.set_palette([secondary_highlight_color, primary_highlight_color])
    hue_order = ['secondary_highlight_group', 'primary_highlight_group']

    plot_data = plot_data.sort_values(by=data_point_id)

    # Plotting swarm plot.
    sns.swarmplot(data=plot_data,
                  x=x_metric,
                  y=y_metric,
                  order=y_groups,
                  color=base_colour,
                  alpha=1,
                  size=point_size - (len(y_groups)),
                  edgecolor=TEXT_COLOR,
                  linewidth=0.1)

    # Plotting swarm plot for highlight data points (larger scatter size).
    if len(primary_highlight_group) > 0 or len(secondary_highlight_group) > 0:
        swarmplots = sns.swarmplot(data=plot_data[plot_data['swarm_group'] != 'background_group'],
                                   x=x_metric,
                                   y=y_metric,
                                   order=y_groups,
                                   hue_order=hue_order,
                                   hue='swarm_group',
                                   alpha=1,
                                   size=highlight_point_size - (len(y_groups)),
                                   edgecolor=TEXT_COLOR,
                                   linewidth=0.3,
                                   zorder=4)

        # Plotting player names for those specified in target or comparison players.
        # Get the positions of the swarm plot on the axis.
        artists = ax.get_children()
        swarmplot_positions = list(range(len(y_groups) * 2, len(y_groups) * 3))

        for i, group in zip(swarmplot_positions, y_groups):
            # Get the data for specific swarm plot.
            group_df = plot_data[plot_data[y_metric] == group].sort_values(by=x_metric, ascending=True).reset_index()
            label_df = group_df[group_df['swarm_group'] != 'background_group'].reset_index()

            # Match the data points to their jitter y position in the swarm plot.
            offsets = swarmplots.collections[i].get_offsets()

            if len(label_df) == len(offsets):
                label_df.loc[:, 'plotted_metric'] = [tup[0] for tup in offsets]
                label_df.loc[:, 'y'] = [tup[1] for tup in offsets]

                # Add texts for target & comparison players.
                texts = [ax.text(label_df[x_metric].iloc[i],
                                 label_df['y'].iloc[i],
                                 str(label_df[data_point_label].iloc[i]),
                                 color=TEXT_COLOR,
                                 fontsize=fontsize,
                                 fontweight='bold',
                                 zorder=6,
                                 path_effects=[pe.withStroke(linewidth=1,
                                                             foreground='white',
                                                             alpha=1)]
                                 ) for i in range(len(label_df))]

                # Plot texts using adjust_text - only adjust spacing in y-axis.
                adjust_text(texts,
                            ax=ax,
                            add_objects=[artists[i]],
                            expand_points=(1, 3),
                            expand_objects=(1, 3),
                            expand_text=(1, 3),
                            force_objects=.75,
                            force_points=.75,
                            force_text=.75,
                            only_move=dict(points='y', text='y', objects='y'),
                            autoalign='y',
                            arrowprops=dict(arrowstyle="-",
                                            color=TEXT_COLOR,
                                            alpha=1,
                                            lw=.5, zorder=2))

    # Adding x-axis label.
    ax.set_xlabel(x_label,
                  fontweight='bold',
                  fontsize=label_fontsize)

    # Removing y-axis labels
    ax.set_ylabel('')

    # Setting tick params.
    ax.tick_params(axis='x',
                   colors=TEXT_COLOR,
                   labelsize=label_fontsize)

    ax.tick_params(axis='y',
                   colors=TEXT_COLOR,
                   labelsize=label_fontsize)

    # Adding y_labels for each categorical group.
    ax.set_yticklabels(y_group_labels,
                       fontweight='bold')

    # Setting x-axis value unit if specified.
    if x_unit is not None:
        formatter0 = EngFormatter(unit=x_unit)
        ax.xaxis.set_major_formatter(formatter0)

    # Setting plot spines to TEXT_COLOR or none.
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color(TEXT_COLOR)
    ax.yaxis.set_ticks_position('none')
    ax.spines['left'].set_color('None')

    # Limiting x-axis if the value is a percentage.
    xmin, xmax = ax.get_xlim()
    if x_unit == '%' and xmax > 110:
        xmin, xmax = ax.get_xlim()
        ax.set_xlim([xmin, 110])

    # Add grid.
    ax.grid(color=TEXT_COLOR,
            axis='both',
            linestyle='--',
            linewidth=0.5,
            alpha=0.25,
            zorder=1)

    # Remove legend.
    ax.legend().remove()

    plt.tight_layout()
    plt.show()

    return fig, ax
