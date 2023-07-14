# %%
import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

SESSION = 'BRITISH'
YEAR = 2023

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

race = fastf1.get_session(YEAR, SESSION, 'R')
race.load()

retired_drivers = race.results.loc[race.results['Status'] != 'Finished']

driver_laps = race.laps.reset_index()
drivers = pd.unique(race.laps['Driver'])

stints = driver_laps[["Driver", "Position", "Stint", "Compound", "LapNumber", "LapTime", "TyreLife"]]

stints['LapTimeSeconds'] = stints['LapTime'].dt.total_seconds().interpolate()
stints.head()

stints['FullName'] = stints['Driver'].map(fastf1.plotting.DRIVER_TRANSLATE)
stints['Color'] = stints['FullName'].map(fastf1.plotting.DRIVER_COLORS)
stints['CumulativeLapTime'] = stints.groupby('Driver')['LapTimeSeconds'].cumsum()

stints.reset_index()

stints['SmallestCumulativeLapTime'] = stints['LapNumber'].map(stints.groupby('LapNumber')['CumulativeLapTime'].min())
stints['IntervalToLeader'] = stints['CumulativeLapTime'] - stints['SmallestCumulativeLapTime']
stints['NormalizedIntervalToLeader'] = stints['CumulativeLapTime'] / stints['SmallestCumulativeLapTime']

stints.reset_index()

stints.to_csv('output.csv')

fig, ax = plt.subplots(ncols=2,figsize=(32,16))

for driver in drivers:
    driver_stint = stints.loc[stints['Driver'] == driver].reset_index()
    driver_color = fastf1.plotting.driver_color(driver)
     
    ax[0].plot(driver_stint["LapNumber"],
            driver_stint["IntervalToLeader"],
            color=driver_color,
            label=driver
           )

ax[0].set_title(f'{SESSION} GP - Interval to Leader')
ax[0].set_xlabel('Lap Number')
ax[0].set_ylabel('Interval to Leader (s)')
ax[0].margins(0.05, 0.1)
ax[0].legend()

for driver in drivers:
    driver_stint = stints.loc[stints['Driver'] == driver].reset_index()
    driver_color = fastf1.plotting.driver_color(driver)
     
    plt.plot(driver_stint["LapNumber"],
            driver_stint["NormalizedIntervalToLeader"],
            color=driver_color,
            label=driver
           )

ax[1].set_title(f'{SESSION} GP - Normalized Interval to Leader')
ax[1].set_xlabel('Lap Number')
ax[1].set_ylabel('Normalized Interval to Leader')
ax[1].margins(0.05, 0.1)
ax[1].legend()

plt.savefig(f'graphs/{YEAR}/{YEAR} {SESSION} GP - Laptimes To Leader.png', format='png')