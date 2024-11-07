"""
Liam Michael Bailey
Helper functions
This file contains functions to help to use SkillCorner physical data.
"""


def add_p90(df, column_name):
    """
    Function to add P90 values for a column.

    Parameters:
        df (DataFrame) : The DataFrame containing the original metrics.
        column_name : The column name which the P90 values will be generated for

    Returns:
        df (DataFrame) : The DataFrame now containing the P90 column
    """
    df[column_name + '_per_90'] = df[column_name + '_full_all'] / (df['minutes_full_all'] / 90)  # Creates new column with the P90 values
    df[column_name + '_per_90'] = df[column_name + '_per_90'].round(1)  # Rounds the values in the column to one decimal place.

    return df


def add_p60_bip(df, column):
    """
    Parameters:
        df (DataFrame) : The DataFrame containing the original metrics.
        column : The column which the BIP per 60 value will be generated for
    """

    # Normalizes BIP per 60 by dividing the BIP column by the number of hours played.
    df[column + '_per_60_bip'] = ((df[column + '_full_tip'] + df[column + '_full_otip'])/
                               (df['minutes_full_tip'] + df['minutes_full_otip'])) * 60


def add_p30_tip(df, column):
    """
    Parameters:
        df (DataFrame) : The DataFrame containing the original metrics.
        column : The column which the TIP per 30 value will be generated for
    """

    # Normalizes TIP per 30 by dividing the TIP column by the number of half-an-hours played.
    df[column + '_per_30_tip'] = (df[column + '_full_tip'] / df['minutes_full_tip']) * 30


def add_p30_otip(df, column):
    """
    Parameters:
        df (DataFrame) : The DataFrame containing the original metrics.
        column : The column which the OTIP per 30 value will be generated for
    """

    # Normalizes OTIP per 30 by dividing the OTIP column by the number of half-an-hours played.
    df[column + '_per_30_otip'] = (df[column + '_full_otip'] / df['minutes_full_otip']) * 30


def add_standard_metrics(df):
    """
    Adds standard metrics to the DataFrame.

    This function calculates and adds various standard metrics to the given DataFrame, including per-90 metrics,
    per-60 BIP metrics, per-30 TIP metrics, and per-30 OTIP metrics. It also adds high-intensity (HI) distance,
    count of high-intensity runs, and several other performance metrics normalized per minute and per sprint.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.

    Returns:
        list: A list of the names of the newly added or modified metrics.
    """

    df['minutes_full_bip'] = df['minutes_full_tip'] + df['minutes_full_otip']

    metrics = []
    metrics.append('minutes_full_all')
    metrics.append('minutes_full_bip')
    metrics.append('minutes_full_tip')
    metrics.append('minutes_full_otip')

    # Adds several columns based of the base metric, as well as TIP, OTIP.
    df['accel_count_full_all'] = df['medaccel_count_full_all'] + df['highaccel_count_full_all']
    df['accel_count_full_tip'] = df['medaccel_count_full_tip'] + df['highaccel_count_full_tip']
    df['accel_count_full_otip'] = df['medaccel_count_full_otip'] + df['highaccel_count_full_otip']

    df['decel_count_full_all'] = df['meddecel_count_full_all'] + df['highdecel_count_full_all']
    df['decel_count_full_tip'] = df['meddecel_count_full_tip'] + df['highdecel_count_full_tip']
    df['decel_count_full_otip'] = df['meddecel_count_full_otip'] + df['highdecel_count_full_otip']

    raw_metrics = ['total_distance',
                   'running_distance',
                   'hsr_distance',
                   'sprint_distance',
                   'hi_distance',
                   'hsr_count',
                   'sprint_count',
                   'hi_count',
                   'accel_count',
                   'highaccel_count',
                   'medaccel_count',
                   'decel_count',
                   'highdecel_count',
                   'meddecel_count']

    # Adds  the BIP, P90, P60 BIP, P30 TIP, P30 OTIP values to each metric in 'raw_metrics'
    for m in raw_metrics:
        add_p90(df, m)
        add_p60_bip(df, m)
        add_p30_tip(df, m)
        add_p30_otip(df, m)

        df[m + '_full_bip'] = df[m + '_full_tip'] + df[m + '_full_otip']

        # Adds each metric, as well as each normalization to the metrics list
        metrics.append(m)
        metrics.append(m + '_per_90')
        metrics.append(m + '_full_bip')
        metrics.append(m + '_per_60_bip')
        metrics.append(m + '_full_tip')
        metrics.append(m + '_per_30_tip')
        metrics.append(m + '_full_otip')
        metrics.append(m + '_per_30_otip')

    # Adds several columns with metrics to the df, as well as their names to the metrics list
    df['meters_per_minute'] = df['total_distance_full_all'] / df['minutes_full_all']
    df['meters_per_minute_bip'] = df['total_distance_full_bip'] / df['minutes_full_bip']
    df['meters_per_minute_tip'] = df['total_distance_full_tip'] / df['minutes_full_tip']
    df['meters_per_minute_otip'] = df['total_distance_full_otip'] / df['minutes_full_otip']
    metrics.append('meters_per_minute')
    metrics.append('meters_per_minute_bip')
    metrics.append('meters_per_minute_tip')
    metrics.append('meters_per_minute_otip')

    df['hi_meters_per_minute'] = df['hi_distance_full_all'] / df['minutes_full_all']
    df['hi_meters_per_minute_bip'] = df['hi_distance_full_bip'] / df['minutes_full_bip']
    df['hi_meters_per_minute_tip'] = df['hi_distance_full_tip'] / df['minutes_full_tip']
    df['hi_meters_per_minute_otip'] = df['hi_distance_full_otip'] / df['minutes_full_otip']
    metrics.append('hi_meters_per_minute')
    metrics.append('hi_meters_per_minute_bip')
    metrics.append('hi_meters_per_minute_tip')
    metrics.append('hi_meters_per_minute_otip')

    df['distance_per_sprint'] = df['sprint_distance_full_all'] / df['sprint_count_full_all']
    df['distance_per_sprint_bip'] = df['sprint_distance_full_bip'] / df['sprint_count_full_bip']
    df['distance_per_sprint_tip'] = df['sprint_distance_full_tip'] / df['sprint_count_full_tip']
    df['distance_per_sprint_otip'] = df['sprint_distance_full_otip'] / df['sprint_count_full_otip']
    metrics.append('distance_per_sprint')
    metrics.append('distance_per_sprint_bip')
    metrics.append('distance_per_sprint_tip')
    metrics.append('distance_per_sprint_otip')

    metrics.append('psv99')

    df['minutes_played_per_match'] = df['minutes_full_all']

    return metrics
