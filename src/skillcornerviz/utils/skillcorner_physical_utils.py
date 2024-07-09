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
    df[column_name + ' P90'] = df[column_name] / (df['minutes_full_all'] / 90)  # Creates new column with the P90 values
    df[column_name + ' P90'] = df[column_name + ' P90'].round(1)  # Rounds the values in the column to one decimal place.

    return df


def add_bip_value(df, column):
    """
    Parameters:
        df (DataFrame) : The DataFrame containing the original metrics.
        column : The column which the BIP value will be generated for
    """

    # Calculate BIP by adding TIP and OTIP values and assign it to a new column in the DataFrame
    df[column + ' BIP'] = df[column + ' TIP'] + df[column + ' OTIP']


def add_p60_bip(df, column):
    """
    Parameters:
        df (DataFrame) : The DataFrame containing the original metrics.
        column : The column which the BIP per 60 value will be generated for
    """

    # Normalizes BIP per 60 by dividing the BIP column by the number of hours played.
    df[column + ' P60 BIP'] = df[column + ' BIP'] / (df['Minutes BIP'] / 60)


def add_p30_tip(df, column):
    """
    Parameters:
        df (DataFrame) : The DataFrame containing the original metrics.
        column : The column which the TIP per 30 value will be generated for
    """

    # Normalizes TIP per 30 by dividing the TIP column by the number of half-an-hours played.
    df[column + ' P30 TIP'] = df[column + ' TIP'] / (df['Minutes TIP'] / 30)


def add_p30_otip(df, column):
    """
    Parameters:
        df (DataFrame) : The DataFrame containing the original metrics.
        column : The column which the OTIP per 30 value will be generated for
    """

    # Normalizes OTIP per 30 by dividing the OTIP column by the number of half-an-hours played.
    df[column + ' P30 OTIP'] = df[column + ' OTIP'] / (df['Minutes OTIP'] / 30)


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

    metrics = []
    add_bip_value(df, 'Minutes')
    metrics.append('Minutes')
    metrics.append('Minutes BIP')
    metrics.append('Minutes TIP')
    metrics.append('Minutes OTIP')

    # Adds several columns based of the base metric, as well as TIP, OTIP.
    df['HI Distance'] = df['Sprinting Distance'] + df['HSR Distance']
    df['HI Distance TIP'] = df['Sprinting Distance TIP'] + df['HSR Distance TIP']
    df['HI Distance OTIP'] = df['Sprinting Distance OTIP'] + df['HSR Distance OTIP']

    df['Count HI'] = df['Count Sprint'] + df['Count HSR']
    df['Count HI TIP'] = df['Count Sprint TIP'] + df['Count HSR TIP']
    df['Count HI OTIP'] = df['Count Sprint OTIP'] + df['Count HSR OTIP']

    df['Count Acceleration'] = df['Count High Acceleration'] + df['Count Medium Acceleration']
    df['Count Acceleration TIP'] = df['Count High Acceleration TIP'] + df['Count Medium Acceleration TIP']
    df['Count Acceleration OTIP'] = df['Count High Acceleration OTIP'] + df['Count Medium Acceleration OTIP']

    df['Count Deceleration'] = df['Count High Deceleration'] + df['Count Medium Deceleration']
    df['Count Deceleration TIP'] = df['Count High Deceleration TIP'] + df['Count Medium Deceleration TIP']
    df['Count Deceleration OTIP'] = df['Count High Deceleration OTIP'] + df['Count Medium Deceleration OTIP']

    raw_metrics = ['Distance',
                   'Running Distance',
                   'HSR Distance',
                   'Sprinting Distance',
                   'HI Distance',
                   'Count HSR',
                   'Count Sprint',
                   'Count HI',
                   'Count Acceleration',
                   'Count High Acceleration',
                   'Count Medium Acceleration',
                   'Count Deceleration',
                   'Count High Deceleration',
                   'Count Medium Deceleration']

    # Adds  the BIP, P90, P60 BIP, P30 TIP, P30 OTIP values to each metric in 'raw_metrics'
    for m in raw_metrics:
        add_bip_value(df, m)
        add_p90(df, m)
        add_p60_bip(df, m)
        add_p30_tip(df, m)
        add_p30_otip(df, m)

        # Adds each metric, as well as each normalization to the metrics list
        metrics.append(m)
        metrics.append(m + ' P90')
        metrics.append(m + ' BIP')
        metrics.append(m + ' P60 BIP')
        metrics.append(m + ' TIP')
        metrics.append(m + ' P30 TIP')
        metrics.append(m + ' OTIP')
        metrics.append(m + ' P30 OTIP')

    # Adds several columns with metrics to the df, as well as their names to the metrics list
    df['Meters per Minute'] = df['Distance'] / df['Minutes']
    df['Meters per Minute BIP'] = df['Distance BIP'] / df['Minutes BIP']
    df['Meters per Minute TIP'] = df['Distance TIP'] / df['Minutes TIP']
    df['Meters per Minute OTIP'] = df['Distance OTIP'] / df['Minutes OTIP']
    metrics.append('Meters per Minute')
    metrics.append('Meters per Minute BIP')
    metrics.append('Meters per Minute TIP')
    metrics.append('Meters per Minute OTIP')

    df['HI Meters per Minute'] = df['HI Distance'] / df['Minutes']
    df['HI Meters per Minute BIP'] = df['HI Distance BIP'] / df['Minutes BIP']
    df['HI Meters per Minute TIP'] = df['HI Distance TIP'] / df['Minutes TIP']
    df['HI Meters per Minute OTIP'] = df['HI Distance OTIP'] / df['Minutes OTIP']
    metrics.append('HI Meters per Minute')
    metrics.append('HI Meters per Minute BIP')
    metrics.append('HI Meters per Minute TIP')
    metrics.append('HI Meters per Minute OTIP')

    df['Distance per Sprint'] = df['Sprinting Distance'] / df['Count Sprint']
    df['Distance per Sprint BIP'] = df['Sprinting Distance BIP'] / df['Count Sprint BIP']
    df['Distance per Sprint TIP'] = df['Sprinting Distance TIP'] / df['Count Sprint TIP']
    df['Distance per Sprint OTIP'] = df['Sprinting Distance OTIP'] / df['Count Sprint OTIP']
    metrics.append('Distance per Sprint')
    metrics.append('Distance per Sprint BIP')
    metrics.append('Distance per Sprint TIP')
    metrics.append('Distance per Sprint OTIP')

    metrics.append('PSV-99')
    if 'player_id' in list(df.columns):
        metrics.append('Top 5 PSV-99')

    df['minutes_played_per_match'] = df['Minutes']

    return metrics
