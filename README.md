# SkillCornerviz  Overview
The SkillCornerviz Library is a Python package that provides functions to create standard visualizations
frequently used by the SkillCorner data analysis team. It also includes functions to normalize SkillCorner data
in various ways. This package is designed to streamline the data analysis process and facilitate the creation
of insightful visualizations.

----------------------------------------------------------------------------------------------------------------------------
# File Structure 
```python
skillcornerviz/
├── resources/
│   └── Roboto/ # Folder containing fonts
│       └── __init__.py
├── standard_plots/
│   ├── __init__.py
│   ├── bar_plot.py
│   ├── formating.py
│   ├── radar_plot.py
│   ├── scatter_plot.py
│   ├── summary_table.py
│   └── swarm_violin_plot.py
├── utils/
│   ├── __init__.py
│   ├── constants.py
│   ├── skillcorner_colors.py
│   ├── skillcorner_game_intelligence_utils.py
│   ├── skillcorner_physical_utils.py
│   └── skillcorner_utils.py
└── __init__.py
```
----------------------------------------------------------------------------------------------------------------------------
# Installation Instructions
- Open the Terminal 
- Ensure python is installed by running the command ```python --version``` through the terminal. 
- Ensure pip is installed by running the command ```pip --version``` through the terminal. 
- Once both python and pip are installed, you can install the package using ```pip install skillcornerviz```. 
- Ensure that the package is installed using ```pip show skillcornerviz``` which will display information about the package if it has been installed. 

----------------------------------------------------------------------------------------------------------------------------

# Plot Examples - Including Code Snippets
## <u>Bar Plot</u>
### Code Snippet:
```python
from skillcornerviz.standard_plots import bar_plot as bar
from src.skillcornerviz.utils import skillcorner_physical_utils as put
from skillcorner.client import SkillcornerClient
import pandas as pd

client = SkillcornerClient(username='YOUR USERNAME', password='YOUR PASSWORD')
data = client.get_physical(params={'competition': 4, 'season': 28,
                                    'group_by': 'player,team,competition,season,group',
                                    'playing_time__gte': 60, 'count_match__gte':8,
                                    'data_version': '3'})

df = pd.DataFrame(data)

real_madrid = df[df['team_id'] == 262]
real_forwards = real_madrid[real_madrid['position_group'].isin(['Wide Attacker', 'Center Forward'])]

yamal_williams = df[df['player_id'].isin([639784, 35342])]

merged_df = pd.concat([real_forwards, yamal_williams], ignore_index=True)
fig, ax = bar.plot_bar_chart(merged_df, 'psv99_top5',data_point_id='team_name',
                             plot_title='Comparison - Real Madrid Forwards VS Nico Williams & Lamine Yamal',
                             label='Top 5 PSV-99 Values', primary_highlight_group=['Athletic Club de Bilbao',
                            'FC Barcelona'], primary_highlight_color='#17D9BA')
```
### Bar Plot Figure:
![standard bar plot](https://github.com/MarkosBont/skillcorner_library_cleanup/blob/34de90fca73d5486a144c00a2c332f9b99561747/example_plots/bar_plot.png)
## <u>Scatter Plot</u>
### Code Snippet:
```python
from skillcornerviz.standard_plots import scatter_plot as scpl
from src.skillcornerviz.utils import skillcorner_physical_utils as put
from skillcorner.client import SkillcornerClient
import pandas as pd


client = SkillcornerClient(username='YOUR USERNAME', password='YOUR PASSWORD')
data = client.get_physical(params={'competition': 4, 'season': 28,
                                    'group_by': 'player,team,competition,season,group',
                                    'playing_time__gte': 60, 'count_match__gte':8,
                                    'data_version': '3'})

df = pd.DataFrame(data)

midfielders = df[df['position_group'].isin(['Midfield'])]

put.add_p90(midfielders, 'total_distance_full_all')
put.add_p90(midfielders, 'hi_distance_full_all')

fig, ax = scpl.plot_scatter(midfielders, x_metric='total_distance_full_all P90',y_metric='hi_distance_full_all P90', data_point_id='team_name',
                            plot_title='Real Madrid VS Barcelona || Midfielders', x_label='Total distance Per 90 (Meters)',
                            y_label="High Intensity Distance Per 90 (Meters)", primary_highlight_group=['FC Barcelona'], primary_highlight_color='#17D9BA',
                            secondary_highlight_group=['Real Madrid CF'], secondary_highlight_color='#9E4DFF')
```
### Scatter Plot Figure
![standard scatter plot](example_plots/scatter_plot.png)

## <u>Radar Plot</u>
### Code Snippet
```python
from skillcornerviz.standard_plots import radar_plot as rad
from skillcorner.client import SkillcornerClient
import pandas as pd

client = SkillcornerClient(username='YOUR_USERNAME', password='YOUR_PASSWORD')

# Request data for LaLiga 2023/2024.
la_liga = client.get_in_possession_off_ball_runs(params={'competition': 4, 'season': 28,
                                                         'playing_time__gte': 60, 'count_match__gte': 8,
                                                         'average_per': '30_min_tip',
                                                         'group_by': 'player,competition,team,group',
                                                         'run_type': 'all,run_in_behind,run_ahead_of_the_ball,'
                                                                     'support_run,pulling_wide_run,coming_short_run,'
                                                                     'underlap_run,overlap_run,dropping_off_run,'
                                                                     'pulling_half_space_run,cross_receiver_run'})

la_liga_df = pd.DataFrame(la_liga)

RUNS = {'count_cross_receiver_runs_per_30_min_tip': 'Cross Receiver',
        'count_runs_in_behind_per_30_min_tip': ' In Behind',
        'count_runs_ahead_of_the_ball_per_30_min_tip': 'Ahead Of The Ball',
        'count_overlap_runs_per_30_min_tip': 'Overlap',
        'count_underlap_runs_per_30_min_tip': 'Underlap',
        'count_support_runs_per_30_min_tip': 'Support',
        'count_coming_short_runs_per_30_min_tip': 'Coming Short',
        'count_dropping_off_runs_per_30_min_tip': 'Dropping Off',
        'count_pulling_half_space_runs_per_30_min_tip': 'Pulling Half-Space',
        'count_pulling_wide_runs_per_30_min_tip': 'Pulling Wide'}

# Plot off-ball run radar for Nico Williams.
fig, ax = rad.plot_radar(la_liga_df[la_liga_df['group'] == 'Wide Attacker'],
                         data_point_id='player_id', label=35342,
                         plot_title='Off-Ball Run Profile | Nico Williams 2023/24',
                         metrics=RUNS.keys(), metric_labels=RUNS, percentiles_precalculated=False,
                         suffix=' Runs P30 TIP', positions='Wide Attackers', matches=8,
                         minutes=60, competitions='LaLiga', seasons='2023/2024', add_sample_info=True)

```
### Radar Plot Figure
![standard radar plot](example_plots/radar_plot.png)

## <u>Summary Table</u>
### Code Snippet
```python
from skillcornerviz.standard_plots import summary_table as sumtab
from src.skillcornerviz.utils import skillcorner_physical_utils as put
from skillcorner.client import SkillcornerClient
import pandas as pd

client = SkillcornerClient(username='YOUR USERNAME', password='YOUR PASSWORD')
la_liga = client.get_physical(params={'competition': 4, 'season': 28,
                                        'group_by': 'player,team,competition,season,group',
                                        'playing_time__gte': 60, 'count_match__gte': 8,
                                        'data_version': '3'})

la_liga_df = pd.DataFrame(la_liga)

put.add_p90(la_liga_df, 'total_distance_full_all')
put.add_p90(la_liga_df, 'hi_distance_full_all')
put.add_p90(la_liga_df, 'hsr_distance_full_all')
put.add_p90(la_liga_df, 'running_distance_full_all')
put.add_p90(la_liga_df, 'sprint_distance_full_all')

RUNS = {'total_distance_full_all P90': 'Total Distance P90',
        'hi_distance_full_all P90' : 'HI Distance P90',
        'hsr_distance_full_all P90' : 'HSR Distance P90',
        'running_distance_full_all P90': 'Running Distance P90',
        'sprint_distance_full_all P90' : 'Sprint Distance P90'}

fig, ax = sumtab.plot_summary_table(la_liga_df, metrics=RUNS.keys(), metric_col_names=RUNS.values(), players=['Axel Witsel', 'Francis Coquelin',
                                                                                                     'Sergi Darder Moll', 'Toni Kroos',
                                                                                                     'Djibril Sow'])
```
### Summary Table Figure
![Standard Summary Table](example_plots/summary_table.png)

## <u>Swarm/Violin Plot</u>
### Code Snippet
```python
from skillcornerviz.standard_plots import swarm_violin_plot as svp
from skillcorner.client import SkillcornerClient
import pandas as pd

client = SkillcornerClient(username='YOUR_USERNAME', password='YOUR_PASSWORD')

data = client.get_in_possession_off_ball_runs(params={'season': 28,
                                                      'competition': 4,
                                                      'group_by': 'player,team,competition,season,group',
                                                      'playing_time__gte': 60, 'count_match__gte': 8
                                                      }
                                              )
df = pd.DataFrame(data)

x_label = 'Threat Per 100 Runs'
y_labels = ['Center Forwards',
            'Midfielders']
x_unit = ''
comparison_players = ['Toni Kroos', 'Djibril Sow', 'Luka Modrić', 'Vinícius José Paixão de Oliveira Júnior',
                      'Artem Dobvyk', 'Eduardo Camavinga', 'Frenkie De Jong', 'Jude Bellingham',
                      'Robert Lewandowski', 'Álvaro Borja Morata Martin', 'Gerard Moreno Balaguero',
                      'Mikel Oyarzabal Ugarte', 'Mikel Merino Zazón']

fig, ax = svp.plot_swarm_violin(df=df,
                                x_metric='runs_threat_per_match',
                                y_metric='group',
                                y_groups=['Center Forward', 'Midfield'],
                                x_label=x_label,
                                y_group_labels=y_labels,
                                x_unit=x_unit,
                                secondary_highlight_group=comparison_players,
                                point_size=7)
```
### Swarm Violin Plot Figure
![standard svp plot](example_plots/swarm_violin_plot.png)

----------------------------------------------------------------------------------------------------------------------------

# Contact
If you encounter any issues, have suggestions, or would like to know more about the SkillCornerviz Library,
please contact us at through this email: liam.bailey@skillcorner.com
