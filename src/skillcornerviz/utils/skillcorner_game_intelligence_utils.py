"""
Liam Michael Bailey
This file includes general helper functions for game intelligence data.
"""

RUN_TYPES = ['runs',
             'build_up_runs',
             'progression_runs',
             'direct_runs',
             'cross_receiver_runs',
             'runs_in_behind',
             'runs_ahead_of_the_ball',
             'overlap_runs',
             'underlap_runs',
             'support_runs',
             'coming_short_runs',
             'dropping_off_runs',
             'pulling_half_space_runs',
             'pulling_wide_runs']

RUN_GROUPS = {'direct_runs': ['cross_receiver_runs',
                              'runs_in_behind'],
              'progression_runs': ['runs_ahead_of_the_ball',
                                   'overlap_runs',
                                   'underlap_runs',
                                   'support_runs'],
              'build_up_runs': ['coming_short_runs',
                                'dropping_off_runs',
                                'pulling_half_space_runs',
                                'pulling_wide_runs']}


def get_per_90(df, metric_per_match):
    """
    Gets per 90 values for a given metric.

    Parameters:
        df (DataFrame): The DataFrame containing the data.
        metric_per_match (str): The name of the column representing the metric per match.

    Returns:
       Pandas Series: The per 90 values calculated for the given metric.
    """
    return df[metric_per_match] / (df['minutes_played_per_match'] / 90)


def get_per_30_tip(df, metric_per_match):
    """
    Gets per 30 while the team is in possession values for a given metric.

    Parameters:
        df (DataFrame): The DataFrame containing the data.
        metric_per_match (str): The name of the column representing the metric per match.

    Returns:
        Series: The per 30 values (while in possession) calculated for the given metric .
    """
    return df[metric_per_match] / (df['adjusted_min_tip_per_match'] / 30)


# Gets p30 tip metrics for all count metrics.
def add_per_30_tip_metrics(df):
    """
    Adds p30 tip metrics for all count metrics per match in the DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing the original count metrics per match.

    Returns:
        list: A list of the names of the newly added p30 tip metrics columns.
        df: The DataFrame with the newly added metrics
    """
    metrics = []
    for col in df.columns:
        if 'count_' in col and 'per_match' in col:
            # Add a new column with the name replaced from 'per_match' to 'per_30_tip'
            df[col.replace('per_match', 'per_30_tip')] = get_per_30_tip(df, col)
            metrics.append(col.replace('per_match', 'per_30_tip'))

    return df, metrics


def add_per_90_metrics(df):
    """
    Adds p90 metrics for all count metrics per match in the DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing the original count metrics per match.

    Returns:
        list: A list of the names of the newly added per-match normalization metrics.
    """
    metrics = []
    for col in df.columns:
        if 'count_' in col and 'per_match' in col:
            # Add a new column with the name replaced from 'per_match' to 'per_90'
            df[col.replace('per_match', 'per_90')] = get_per_90(df, col)
            metrics.append(col.replace('per_match', 'per_90'))

    return df, metrics


def add_pass_normalisations(df):
    """
    Adds various pass normalization metrics to the DataFrame.

    This function calculates and adds per 90 minutes metrics, per 30 TIP metrics, and several pass ratios
    for different run types to the given DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.

    Returns:
        list: A list of the names of the newly added pass normalization metrics.

    """
    metrics = []

    # Add per 90 metrics to the dataframe and update the list of metrics
    df, per_90_metrics = add_per_90_metrics(df)
    metrics += per_90_metrics

    # Add per 30 TIP metrics to the dataframe and update the list of metrics
    df, per_30_tip_metrics = add_per_30_tip_metrics(df)
    metrics += per_30_tip_metrics

    for run in RUN_TYPES:
        if 'count_opportunities_to_pass_to_' + run + '_per_match' in list(df.columns):

            # Below we calculate the ratios of all types of passes for this run type and add it to the df and metrics list

            df[run + '_pass_attempt_ratio'] = (df['count_pass_attempts_to_' + run + '_per_match'] /
                                               (df['count_opportunities_to_pass_to_' + run + '_per_match'])) * 100
            metrics.append(run + '_pass_attempt_ratio')

            df[run + '_pass_completion_ratio'] = (df['count_completed_pass_to_' + run + '_per_match'] /
                                                  (df['count_pass_attempts_to_' + run + '_per_match'])) * 100
            metrics.append(run + '_pass_completion_ratio')

            df[run + '_pass_serve_ratio'] = (df['count_completed_pass_to_' + run + '_per_match'] /
                                             (df['count_opportunities_to_pass_to_' + run + '_per_match'])) * 100
            metrics.append(run + '_pass_serve_ratio')

            df[run + '_dangerous_pass_attempt_ratio'] = (df['count_pass_attempts_to_dangerous_' + run + '_per_match'] /
                                                         (df[
                                                             'count_pass_opportunities_to_dangerous_' + run + '_per_match'])) * 100
            metrics.append(run + '_dangerous_pass_attempt_ratio')

            df[run + '_dangerous_pass_completion_ratio'] = (df[
                                                                'count_completed_pass_to_dangerous_' + run + '_per_match'] /
                                                            (df[
                                                                'count_pass_attempts_to_dangerous_' + run + '_per_match'])) * 100
            metrics.append(run + '_dangerous_pass_completion_ratio')

            df[run + '_dangerous_pass_serve_ratio'] = (df['count_completed_pass_to_dangerous_' + run + '_per_match'] /
                                                       (df[
                                                           'count_pass_opportunities_to_dangerous_' + run + '_per_match'])) * 100
            metrics.append(run + '_dangerous_pass_serve_ratio')

            df[run + '_threat_per_100_pass_attempts'] = (df[run + '_to_which_pass_attempted_threat_per_match'] /
                                                         (df['count_pass_attempts_to_' + run + '_per_match'] / 100))
            metrics.append(run + '_threat_per_100_pass_attempts')

            df[run + '_threat_per_100_completed_passes'] = (df[run + '_to_which_pass_completed_threat_per_match'] /
                                                            (df['count_completed_pass_to_' + run + '_per_match'] / 100))
            metrics.append(run + '_threat_per_100_completed_passes')

    return metrics


def add_run_normalisations(df):
    """
    Adds various run normalization metrics to the DataFrame.

    This function calculates and adds per 90 minutes metrics, per 30 TIP metrics, and several run percentages
    for different run types to the given DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.

    Returns:
        list: A list of the names of the newly added run normalization metrics.

    """
    metrics = []

    # Add per 90 metrics to the dataframe and update the list of metrics
    df, per_90_metrics = add_per_90_metrics(df)
    metrics += per_90_metrics

    # Add per 30 TIP metrics to the dataframe and update the list of metrics
    df, per_30_tip_metrics = add_per_30_tip_metrics(df)
    metrics += per_30_tip_metrics

    for run in RUN_TYPES:
        if 'count_' + run + '_per_match' in list(df.columns):

            # Calculates various p90, p30 TIP metrics and run-related percentages e.g., target, receive, serve, dangerous),
            # then adds these to the data frame, as well as appends them to the metrics list

            df[run + '_threat_per_100'] = df[run + '_threat_per_match'] / (
                    df['count_' + run + '_per_match'] / 100)

            metrics.append(run + '_threat_per_100')

            df[run + '_target_percentage'] = (df['count_' + run + '_targeted_per_match'] /
                                              df['count_' + run + '_per_match']) * 100

            metrics.append(run + '_target_percentage')

            df[run + '_receive_percentage'] = (df['count_' + run + '_received_per_match'] /
                                               df['count_' + run + '_targeted_per_match']) * 100

            metrics.append(run + '_receive_percentage')

            df[run + '_serve_percentage'] = (df['count_' + run + '_received_per_match'] /
                                             df['count_' + run + '_per_match']) * 100

            metrics.append(run + '_serve_percentage')

            # Dangerous Runs
            df['dangerous_' + run + '_target_percentage'] = (df['count_dangerous_' + run + '_targeted_per_match'] /
                                                             df['count_dangerous_' + run + '_per_match']) * 100

            metrics.append('dangerous_' + run + '_target_percentage')

            df['dangerous_' + run + '_receive_percentage'] = (df['count_dangerous_' + run + '_received_per_match'] /
                                                              df[
                                                                  'count_dangerous_' + run + '_targeted_per_match']) * 100

            metrics.append('dangerous_' + run + '_receive_percentage')

            df['dangerous_' + run + '_serve_percentage'] = (df['count_dangerous_' + run + '_received_per_match'] /
                                                            df['count_dangerous_' + run + '_per_match']) * 100

            metrics.append('dangerous_' + run + '_serve_percentage')

            df[run + '_leading_to_shot_percentage_all_runs'] = (df['count_' + run + '_leading_to_shot_per_match'] /
                                                                df['count_' + run + '_per_match']) * 100

            metrics.append(run + '_leading_to_shot_percentage_all_runs')

            df[run + '_leading_to_goal_percentage_all_runs'] = (df['count_' + run + '_leading_to_goal_per_match'] /
                                                                df['count_' + run + '_per_match']) * 100

            metrics.append(run + '_leading_to_goal_percentage_all_runs')

            df[run + '_leading_to_shot_percentage_received_runs'] = (df['count_' + run + '_leading_to_shot_per_match'] /
                                                                     df['count_' + run + '_received_per_match']) * 100

            metrics.append(run + '_leading_to_shot_percentage_received_runs')

            df[run + '_leading_to_goal_percentage_received_runs'] = (df['count_' + run + '_leading_to_goal_per_match'] /
                                                                     df['count_' + run + '_received_per_match']) * 100

            metrics.append(run + '_leading_to_goal_percentage_received_runs')

            df[run + '_dangerous_percentage'] = (df['count_dangerous_' + run + '_per_match'] /
                                                 df['count_' + run + '_per_match']) * 100

            metrics.append(run + '_dangerous_percentage')

    return metrics


# Adds metrics for build up, progression & direct runs.
def add_run_groups(df):
    """
    Adds aggregated run metrics to the DataFrame based on predefined run groups.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.

    Returns:
        DataFrame: The DataFrame with the newly added aggregated run metrics.
    """
    for key in RUN_GROUPS:

        # Calculates various aggregated run metrics (e.g., counts per match, targeted per match,
        # received per match, leading to shot per match, leading to goal per match, dangerous counts per match,
        # and threat per match) for predefined run groups and adds them to the given DataFrame.

        df['count_' + key + '_in_sample'] = df[
            ['count_' + type + '_in_sample' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_' + key + '_per_match'] = df[
            ['count_' + type + '_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_' + key + '_targeted_per_match'] = df[
            ['count_' + type + '_targeted_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_' + key + '_received_per_match'] = df[
            ['count_' + type + '_received_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_' + key + '_leading_to_shot_per_match'] = df[
            ['count_' + type + '_leading_to_shot_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_' + key + '_leading_to_goal_per_match'] = df[
            ['count_' + type + '_leading_to_goal_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_dangerous_' + key + '_per_match'] = df[
            ['count_dangerous_' + type + '_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_dangerous_' + key + '_targeted_per_match'] = df[
            ['count_dangerous_' + type + '_targeted_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_dangerous_' + key + '_received_per_match'] = df[
            ['count_dangerous_' + type + '_received_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df[key + '_threat_per_match'] = df[
            [type + '_threat_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)

    return df


def add_pass_groups(df):
    """
    Adds aggregated run metrics to the DataFrame based on predefined pass groups.

    Parameters:
        df (DataFrame): The DataFrame containing the original metrics.

    Returns:
        DataFrame: The DataFrame with the newly added aggregated pass metrics.
    """
    for key in RUN_GROUPS:

        # Calculates various aggregated pass metrics (e.g., count_opportunities_to_pass_to, count_pass_attempts_to,
        # count_completed_pass_to, count_pass_attempts_to_dangerous etc.)
        # for predefined run groups and adds them to the given DataFrame.

        df['count_opportunities_to_pass_to_' + key + '_in_sample'] = df[
            ['count_opportunities_to_pass_to_' + type + '_in_sample' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_opportunities_to_pass_to_' + key + '_per_match'] = df[
            ['count_opportunities_to_pass_to_' + type + '_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_pass_attempts_to_' + key + '_per_match'] = df[
            ['count_pass_attempts_to_' + type + '_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_completed_pass_to_' + key + '_per_match'] = df[
            ['count_completed_pass_to_' + type + '_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_pass_opportunities_to_dangerous_' + key + '_per_match'] = df[
            ['count_pass_opportunities_to_dangerous_' + type + '_per_match' for type in RUN_GROUPS[key]]].sum(
            axis=1)
        df['count_pass_attempts_to_dangerous_' + key + '_per_match'] = df[
            ['count_pass_attempts_to_dangerous_' + type + '_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_completed_pass_to_dangerous_' + key + '_per_match'] = df[
            ['count_completed_pass_to_dangerous_' + type + '_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df[key + '_to_which_pass_attempted_threat_per_match'] = df[
            [type + '_to_which_pass_attempted_threat_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df[key + '_to_which_pass_completed_threat_per_match'] = df[
            [type + '_to_which_pass_completed_threat_per_match' for type in RUN_GROUPS[key]]].sum(axis=1)
        df['count_completed_pass_to_' + key + '_leading_to_shot_per_match'] = df[
            ['count_completed_pass_to_' + type + '_leading_to_shot_per_match' for type in RUN_GROUPS[key]]].sum(
            axis=1)
        df['count_completed_pass_to_' + key + '_leading_to_goal_per_match'] = df[
            ['count_completed_pass_to_' + type + '_leading_to_goal_per_match' for type in RUN_GROUPS[key]]].sum(
            axis=1)

    return df
