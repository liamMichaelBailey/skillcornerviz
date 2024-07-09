import unittest
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from src.skillcornerviz.standard_plots.bar_plot import plot_bar_chart
from skillcorner.client import SkillcornerClient
from src.skillcornerviz.standard_plots import scatter_plot as sca
from src.skillcornerviz.standard_plots import swarm_violin_plot as svp, bar_plot as bar, \
    radar_plot as rad, summary_table as sum
from src.skillcornerviz.utils import skillcorner_game_intelligence_utils as gi
from src.skillcornerviz.utils import skillcorner_physical_utils as pu

client = SkillcornerClient(username='YOUR USERNAME', password='YOUR PASSWORD')


######################
#    PLOT TESTING
######################

class BarPlot(unittest.TestCase):
    def setUp(self):
        stats = client.get_physical(params={'match': 1498966, 'api_version': 'v2'})
        self.df = pd.DataFrame(stats)

    def test_bar_plot_return_type(self):
        fig, ax = bar.plot_bar_chart(df=self.df, metric='Distance', label='Distance of each player')
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)

    def test_plot_title(self):
        title = 'Distance of each player'
        fig, ax = plot_bar_chart(self.df, 'Distance', plot_title=title)
        self.assertEqual(ax.get_title(), title, )


class RadarPlot(unittest.TestCase):

    def setUp(self):
        runs = client.get_in_possession_off_ball_runs(params={'season': 28,
                                                              'competition': [1],
                                                              'playing_time__gte': 60,
                                                              'average_per': '30_min_tip',
                                                              'group_by': 'player,competition,team,group',
                                                              'run_type': 'all,run_in_behind,run_ahead_of_the_ball,support_run,pulling_wide_run,coming_short_run,underlap_run,overlap_run,dropping_off_run,pulling_half_space_run,cross_receiver_run'})
        self.df = pd.DataFrame(runs)

    def test_radar_plot_return_type(self):
        run_types = {
            'count_cross_receiver_runs_per_30_min_tip': 'Cross Receiver Runs',
            'count_runs_in_behind_per_30_min_tip': 'Runs in behind',
            'count_runs_ahead_of_the_ball_per_30_min_tip': 'Runs Ahead of the ball',
            'count_overlap_runs_per_30_min_tip': 'Overlap Runs',
            'count_underlap_runs_per_30_min_tip': 'Underlap Runs',
            'count_support_runs_per_30_min_tip': 'Support Runs',
            'count_coming_short_runs_per_30_min_tip': 'Coming short Runs',
            'count_dropping_off_runs_per_30_min_tip': 'Dropping Off Runs',
            'count_pulling_half_space_runs_per_30_min_tip': 'Pulling Half-space Runs',
            'count_pulling_wide_runs_per_30_min_tip': 'Pulling Wide Runs'
        }

        fig, ax = rad.plot_radar(df=self.df, label='Alexander Isak', metrics=run_types.keys(),
                                 metric_labels=run_types, plot_title='Alexander Isak | Newcastle | ST',
                                 percentiles_precalculated=False)
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)


class ScatterPlot(unittest.TestCase):
    def setUp(self):
        stats = client.get_physical(params={'match': 1498966, 'api_version': 'v2'})
        self.df = pd.DataFrame(stats)

    def test_scatter_plot_return_type(self):
        fig, ax = sca.plot_scatter(df=self.df, x_metric='Distance 1', y_metric='Distance 2',
                                   x_label='First Half Distance', y_label='Second Half Distance')
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)

    def test_plot_title(self):
        title = 'Distance of each player'
        fig, ax = plot_bar_chart(self.df, 'Distance', plot_title=title)
        self.assertEqual(ax.get_title(), title, )


class SummaryTable(unittest.TestCase):
    def setUp(self):
        stats = client.get_physical(params={'match': 1498966, 'api_version': 'v2'})
        self.df = pd.DataFrame(stats)

    def test_summary_table_return_type(self):
        fig, ax = sum.plot_summary_table(df=self.df, metrics=['Distance 1', 'Distance 2'],
                                         metric_col_names=['Distance 1', 'Distance 2'],
                                         players=['Antonio Rüdiger', 'Arda Güler'])
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)


class SwarmViolinPlot(unittest.TestCase):
    def setUp(self):
        stats = client.get_physical(params={'match': 1498966, 'api_version': 'v2'})
        self.df = pd.DataFrame(stats)

    def test_svp_return_type(self):
        fig, ax = svp.plot_swarm_violin(df=self.df, x_metric='Distance 1', y_metric='Distance 2',
                                        x_label='First Half Distance')
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)


#####################
#  GI & PU Testing
#####################


class GetPer90(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric_per_match': [100, 200, 300],
            'minutes_played_per_match': [90, 180, 270]
        })

    def test_get_per_90(self):
        expected_output = pd.Series([100.0, 100.0, 100.0])
        result = gi.get_per_90(self.df, 'metric_per_match')
        pd.testing.assert_series_equal(result, expected_output)


class GetPer30TIP(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric_per_match': [100, 200, 300],
            'adjusted_min_tip_per_match': [10, 50, 90]
        })

    def test_ger_per_30_tip(self):
        expected_output = pd.Series([300.0, 120.0, 100.0])
        result = gi.get_per_30_tip(self.df, 'metric_per_match')
        pd.testing.assert_series_equal(result, expected_output)


class AddPer30TIP(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'count_metric_per_match': [100, 200, 60],
            'adjusted_min_tip_per_match': [10, 60, 90]
        })

    def test_add_per_30_tip(self):
        expected_col = ['count_metric_per_30_tip']
        expected_df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'count_metric_per_match': [100, 200, 60],
            'adjusted_min_tip_per_match': [10, 60, 90],
            'count_metric_per_30_tip': [300.0, 100.0, 20.0]
        })

        result_df, metrics = gi.add_per_30_tip_metrics(self.df)

        self.assertEqual(expected_col, metrics)
        pd.testing.assert_frame_equal(result_df, expected_df)


class AddPer90(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'count_metric_per_match': [100, 200, 60],
            'minutes_played_per_match': [45, 30, 90]
        })

    def test_add_per_90_metrics(self):
        expected_col = ['count_metric_per_90']
        expected_df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'count_metric_per_match': [100, 200, 60],
            'minutes_played_per_match': [45, 30, 90],
            'count_metric_per_90': [200.0, 600.0, 60.0]
        })

        result_df, metrics = gi.add_per_90_metrics(self.df)

        self.assertEqual(expected_col, metrics)
        pd.testing.assert_frame_equal(result_df, expected_df)


class PhysicalUtils(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric': [100, 200, 60],
            'Minutes': [45, 30, 90],
        })

    def test_add_p90(self):
        expected_df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric': [100, 200, 60],
            'Minutes': [45, 30, 90],
            'metric P90': [200.0, 600.0, 60.0],
        })
        df = pu.add_p90(self.df, 'metric')

        pd.testing.assert_frame_equal(expected_df, df)


class AddBIP(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric TIP': [50, 30, 20],
            'metric OTIP': [20, 50, 30],
            'Minutes': [45, 30, 90],
            'metric P90': [200, 600, 60]
        })

    def test_add_bip_value(self):
        expected_df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric TIP': [50, 30, 20],
            'metric OTIP': [20, 50, 30],
            'Minutes': [45, 30, 90],
            'metric P90': [200, 600, 60],
            'metric BIP': [70, 80, 50]
        })

        pu.add_bip_value(self.df, 'metric')

        pd.testing.assert_frame_equal(self.df, expected_df)


class AddP60BIP(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric BIP': [50, 30, 20],
            'Minutes BIP': [20, 30, 60],
            'metric': [200, 600, 60]
        })

    def test_add_bip_p60_value(self):
        # Same exact test for add_p30_tip(df, column), add_p30_otip(df, column)
        expected_df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric BIP': [50, 30, 20],
            'Minutes BIP': [20, 30, 60],
            'metric': [200, 600, 60],
            'metric P60 BIP': [150.0, 60.0, 20.0]
        })

        pu.add_p60_bip(self.df, 'metric')

        pd.testing.assert_frame_equal(self.df, expected_df)


if __name__ == '__main__':
    unittest.main()
