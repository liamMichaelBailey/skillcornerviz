"""
Markos Bontozoglou
12/06/2024
Radar Plot
The plot_radar function is used to generate a radar plot based on the given data.
It accepts various parameters such as the DataFrame (df), then the list of metrics
to be displayed (metrics), the labels that are given to each metric (metric_labels),
and many stylistic features such as labels, highlighting, theme etc.
"""

from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from skillcornerviz.utils.constants import BASE_COLOR, PRIMARY_HIGHLIGHT_COLOR, FIVE_COLORS, \
    DARK_PRIMARY_HIGHLIGHT_COLOR, SECONDARY_HIGHLIGHT_COLOR
from skillcornerviz.utils.constants import TEXT_COLOR
from skillcornerviz.utils.skillcorner_utils import add_percentile_values
from skillcornerviz.standard_plots import formating
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


def plot_radar(df, label, metrics, plot_title=None, metric_labels=None, simplify_labels=True,
               add_sample_info=False, positions=None, seasons=None, minutes=None, matches=None, competitions=None,
               theme='white', filter_relevant=False, relevant_threshold=0.3, excluded_metrics=None,
               color_groups=None, categorized=None, percentiles_precalculated=True, text_multiplier=1.45,
               rounding=1, suffix='', data_point_id='player_name', secondary_highlight_color=False):
    """
    Create a radar plot to visualize multivariate data using Matplotlib.

    Parameters:
    - df (DataFrame): The input data in the form of a DataFrame.
    - label: The label for the radar plot.
    - metrics: List of metrics to display on the radar plot.
    - plot_title: Title for the radar plot.
    - metric_labels: Labels for the metrics.
    - simplify_labels: If True, simplify metric labels.
    - add_sample_info: If True, add information about data sample.
    - positions, seasons, minutes, matches, competitions: Additional information for the sample.
    - theme: Color theme for the radar plot (e.g., 'white' or 'Dark').
    - filter_relevant: If True, filter out irrelevant metrics.
    - relevant_threshold: Threshold for relevance filtering.
    - excluded_metrics: Metrics to exclude from the plot.
    - color_groups: Custom color groups for metrics.
    - categorized: Categorization of metrics.
    - percentiles_precalculated: If True, use precalculated percentiles.
    - text_multiplier: Multiplier for text size.
    - rounding: Number of decimal places to round the values.
    - suffix: Suffix for values.
    - data_point_id: Identifier for data points.
    - secondary_highlight_color: If True, use a secondary highlight color.

    Returns:
    - fig (Figure): The Matplotlib figure.
    - ax (Axes): The Matplotlib axes.
    """

    # Formatting colours and themes
    if theme == 'Dark':
        primary_color = TEXT_COLOR
        secondary_color = "white"
        bar_color = DARK_PRIMARY_HIGHLIGHT_COLOR
    else:
        primary_color = "white"
        secondary_color = TEXT_COLOR
        bar_color = PRIMARY_HIGHLIGHT_COLOR if secondary_highlight_color is False else SECONDARY_HIGHLIGHT_COLOR

    color_std_palette = FIVE_COLORS

    if excluded_metrics is None:
        excluded_metrics = []
    greyed_metrics = excluded_metrics.copy()

    if filter_relevant:
        for i in metrics:
            # Calculate the ratio of data points with values greater than or equal to 1
            if len(df[df[i] >= 1]) / len(df) < relevant_threshold:
                # If ratio iss less than the relevant_threshold, the metric is added to the list
                greyed_metrics.append(i)

    if color_groups is None:
        # If no color group is given, assign them based on which metrics are greyed out.
        radar_color = [BASE_COLOR if i in greyed_metrics else bar_color for i in metrics]
    else:
        radar_color = color_groups

    volume_metrics = [i for i in metrics]  # Assigns each element in metrics to volume_metrics
    volume_pct_metrics = [i + '_pct' for i in metrics]  # Adds '_pct' to the end of each metric in a new array

    if not percentiles_precalculated:
        add_percentile_values(df, metrics)

    volume_values = df.loc[df[data_point_id] == label][volume_metrics].astype(float).values.tolist()[0]
    volume_pct = df.loc[df[data_point_id] == label][volume_pct_metrics].astype(float).values.tolist()[0]

    # Calculate the width and theta for the radar plot
    width = 6.28319 / len(metrics)
    theta = np.linspace(0, (2 * np.pi), len(metrics), endpoint=False)
    theta = list(theta)
    theta.insert(0, theta.pop(-1))

    # Format the plot figure and axes
    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot(projection='polar')

    # Support dark/light mode
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # Don't change this.
    # Angular axis starts at 90 degrees, not at 0
    ax.set_theta_offset(np.pi / 2)
    # Reverse the direction to go counter-clockwise.
    ax.set_theta_direction(-1)

    # Plot the filled radar bars with specified width, color, and alpha
    ax.bar(theta, volume_pct, width=width, bottom=10,
           color=radar_color,
           edgecolor=None,
           lw=2,
           zorder=3,
           alpha=.95
           )

    # Plot only the edges of the radar bar for the outlines
    ax.bar(theta, volume_pct, width=width, bottom=10, fill=False,
           edgecolor=primary_color,
           lw=2, zorder=5)

    # Adjust the opacity of each bar according to whether it is greyed or not (if the filter is relevant).
    if filter_relevant:
        for bar, name in zip(ax.containers[0], metrics):
            if name in greyed_metrics:
                bar.set_alpha(0.5 if theme == 'white' else 0.1)

    if categorized is not None:
        categories = categorized
        plot_categories = [categories[type] for type in metrics]
        unique_categories = list(set(plot_categories))  # Extracting unique categories

        # Assign colors to bars based on categories
        for volume_bar, volume, category in zip(ax.containers[0], volume_values, plot_categories):
            for i in range(len(unique_categories)):
                if category == unique_categories[i]:
                    volume_bar.set_color(color_std_palette[i])

        # Add legend for categorized data
        for i in range(len(unique_categories)):
            ax.scatter([], [], c=color_std_palette[i], s=200,
                       lw=0.5, edgecolor=secondary_color, zorder=3,
                       label=unique_categories[i])

        # Customise the legend
        ax.legend(facecolor=primary_color,
                  edgecolor=primary_color,
                  framealpha=0.6,
                  labelcolor=secondary_color,
                  fontsize=8 * text_multiplier,
                  loc='upper center',
                  bbox_to_anchor=(0.5, 1.06),
                  ncol=3)

    # Formatting the plot
    ax.set_ylim(0, 120)

    ax.set_yticks([35, 60, 85, 110])
    ax.set_yticklabels(['', '', '', ''])

    pos = ax.get_rlabel_position()
    ax.set_rlabel_position(pos + 106.5)

    y_pos = [35, 60, 85]
    labels = ['25', '50', '75']
    y_axis_pos = min(theta, key=lambda x: abs(x - 1.8))

    # Adding the percentile labels
    for y, l in zip(y_pos, labels):
        ax.text(y_axis_pos + (width * .5),
                y,
                l,
                ha='center',
                va='center',
                size=7 * text_multiplier,
                fontweight='bold',
                color=secondary_color,
                zorder=8,
                path_effects=[pe.withStroke(linewidth=3,
                                            foreground=primary_color,
                                            alpha=1)])

    ax.text(y_axis_pos + (width * .5),
            110,
            '100th\nPercentile',
            ha='left',
            va='center',
            size=7 * text_multiplier,
            color=secondary_color,
            fontweight='bold',
            zorder=8,
            path_effects=[pe.withStroke(linewidth=3,
                                        foreground=primary_color,
                                        alpha=1)])

    ax.set_xticks(theta)

    # Adds the metric labels
    if metric_labels is not None:
        if simplify_labels is False:
            xtick_labels = [metric_labels[i] for i in metrics]
            greyed_metrics_labels = [metric_labels[i] for i in greyed_metrics]
        else:
            xtick_labels = [formating.simplify_label(metric_labels[i]) for i in metrics]
            greyed_metrics_labels = [formating.simplify_label(metric_labels[i]) for i in greyed_metrics]
    else:
        xtick_labels = [formating.prep_label_for_radar(i) for i in metrics]
        greyed_metrics_labels = [formating.prep_label_for_radar(i) for i in greyed_metrics]

    # Initiate labels
    ax.set_xticklabels(xtick_labels,
                       size=8 * text_multiplier,
                       color=secondary_color)

    labels = []

    # Create new labels at the position of the label
    for tick_label, run_type, angle, value_pct in zip(ax.get_xticklabels(), metrics, theta, volume_pct):
        x, y = tick_label.get_position()
        lab = ax.text(x, y,
                      tick_label.get_text(),
                      transform=tick_label.get_transform(),
                      ha=tick_label.get_ha(),
                      va=tick_label.get_va())

        if (90 >= (angle * 180 / np.pi) >= 0) | (360 >= (angle * 180 / np.pi) >= 270):
            lab.set_rotation(0 - (angle * 180 / np.pi))
        else:
            lab.set_rotation(180 - (angle * 180 / np.pi))

        lab.set_y(0.08)
        lab.set_fontproperties({'weight': 'bold', 'size': 10 * text_multiplier})
        lab.set_horizontalalignment('center')

        if tick_label.get_text() in greyed_metrics_labels:
            lab.set_color(BASE_COLOR)
        else:
            lab.set_color(bar_color)

        labels.append(lab)

    # Remove original labels
    ax.set_xticklabels([])

    # Adds the value
    for volume_value, theta, metric in zip(volume_values, theta, volume_metrics):
        volume_text = ax.text(theta,
                              105,
                              str(round(volume_value, rounding)) + suffix,
                              ha='center',
                              va='center',
                              fontweight='bold',
                              color=BASE_COLOR if metric in greyed_metrics else secondary_color,
                              fontsize=8 * text_multiplier,
                              zorder=5,
                              path_effects=[pe.withStroke(linewidth=3,
                                                          foreground=primary_color,
                                                          alpha=1)])

        if (90 >= (theta * 180 / np.pi) >= 0) | (360 >= (theta * 180 / np.pi) >= 270):
            volume_text.set_rotation(0 - (theta * 180 / np.pi))
        else:
            volume_text.set_rotation(180 - (theta * 180 / np.pi))

    ax.xaxis.grid(False)
    ax.yaxis.grid(color=secondary_color, linestyle='--', linewidth=1)
    ax.spines["start"].set_color("none")
    ax.spines["polar"].set_color("none")

    if add_sample_info:
        # add credits
        CREDIT_1 = "Positions: " + positions
        CREDIT_2 = "Seasons: " + seasons
        CREDIT_3 = "Competitions: " + competitions
        CREDIT_4 = "Minimum of " + str(matches) + " matches of at least " + str(minutes) + " minutes"

        # Adding description of the sample information
        ax.text(3.9, 180,
                f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}\n{CREDIT_4}",
                size=8 * text_multiplier,
                color=secondary_color,
                ha="left")

    # Adding a title to the plot
    ax.text(0,
            138,
            label if plot_title is None else plot_title,
            size=14 * text_multiplier,
            color=secondary_color,
            fontweight='bold',
            ha='center')

    # Adding a filter if one was chosen
    if filter_relevant:
        ax.scatter([], [], c=bar_color, s=200,
                   lw=0.5, edgecolor=primary_color, zorder=3,
                   label='Position Relevant')
        ax.scatter([], [], c=BASE_COLOR, s=200, alpha=0.5 if theme == 'white' else 0.1,
                   lw=0.5, edgecolor=primary_color, zorder=3,
                   label='Non-relevant')

        # Adding legend.
        ax.legend(facecolor=primary_color,
                  edgecolor=primary_color,
                  framealpha=0.6,
                  labelcolor=secondary_color,
                  fontsize=8 * text_multiplier,
                  loc='upper center',
                  bbox_to_anchor=(0.5, 1.06),
                  ncol=3)

    plt.tight_layout()
    plt.show()

    return fig, ax
