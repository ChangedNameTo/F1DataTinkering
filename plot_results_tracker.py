import pandas as pd
import matplotlib.pyplot as plt
from fastf1.ergast import Ergast

YEAR = 2023

ergast = Ergast()
races = ergast.get_race_schedule(YEAR)  
results = []

for rnd, race in races['raceName'].items():

    # Get results. Note that we use the round no. + 1, because the round no.
    # starts from one (1) instead of zero (0)
    temp = ergast.get_race_results(season=YEAR, round=rnd + 1)
    
    if len(temp.content):
        temp = temp.content[0]
    else:
        break

    # If there is a sprint, get the results as well
    sprint = ergast.get_sprint_results(season=YEAR, round=rnd + 1)
    if sprint.content and sprint.description['round'][0] == rnd + 1:
        temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
        # Add sprint points and race points to get the total
        temp['points'] = temp['points_x'] + temp['points_y']
        temp.drop(columns=['points_x', 'points_y'], inplace=True)

    # Add round no. and grand prix name
    temp['round'] = rnd + 1
    temp['race'] = race.removesuffix(' Grand Prix')
    temp = temp[['round', 'race', 'driverCode', 'points']]  # Keep useful cols.
    results.append(temp)

# Append all races into a single dataframe
results = pd.concat(results)
races = results['race'].drop_duplicates()

##############################################################################
# Then we “reshape” the results to a wide table, where each row represents a
# driver and each column refers to a race, and the cell value is the points.
results = results.pivot(index='driverCode', columns='round', values='points')
# Here we have a 22-by-22 matrix (22 races and 22 drivers, incl. DEV and HUL)

# Rank the drivers by their total points
results['total_points'] = results.sum(axis=1)
results = results.sort_values(by='total_points', ascending=False)
results.drop(columns='total_points', inplace=True)

# Use race name, instead of round no., as column names
results.columns = races

fig, ax = plt.subplots()

# The final step is to plot a heatmap using plotly
fig = ax.imshow(
    results,
    aspect='auto'
)

# fig.set_ylabel(title_text='')      # Remove axis titles
# fig.set_xlabel(title_text='')
# fig.update_yaxes(tickmode='linear')  # Show all ticks, i.e. driver names
# fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
#                  showline=False,
#                  tickson='boundaries')              # Show horizontal grid only
# fig.update_xaxes(showgrid=False, showline=False)    # And remove vertical grid
# fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')     # White background
# fig.update_layout(coloraxis_showscale=False)        # Remove legend
# fig.update_layout(xaxis=dict(side='top'))           # x-axis on top
# fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins

plt.savefig(f'graphs/{YEAR}/{YEAR} Driver Points by Race.png', format='png')