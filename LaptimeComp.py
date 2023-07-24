import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

SESSION = 'HUNGARIAN'
YEAR = 2023

race = fastf1.get_session(YEAR, SESSION, 'R')
race.load()

def generate_laptime_comp(race, year, session, drivers):
    driver_laps = race.laps.reset_index()
    driver_laps = driver_laps.loc[driver_laps['Driver'].isin(drivers)]

    stints = driver_laps[["Driver", "Position", "Stint", "Compound", "LapNumber", "LapTime", "TyreLife"]]

    stints['LapTimeSeconds'] = stints['LapTime'].dt.total_seconds().interpolate()

    stints['FullName'] = stints['Driver'].map(fastf1.plotting.DRIVER_TRANSLATE)
    stints['Color'] = stints['FullName'].map(fastf1.plotting.DRIVER_COLORS)
    stints['CumulativeLapTime'] = stints.groupby('Driver')['LapTimeSeconds'].cumsum()

    stints.reset_index()

    stints['SmallestCumulativeLapTime'] = stints['LapNumber'].map(stints.groupby('LapNumber')['CumulativeLapTime'].min())
    stints['IntervalToLeader'] = stints['CumulativeLapTime'] - stints['SmallestCumulativeLapTime']
    stints['NormalizedIntervalToLeader'] = stints['CumulativeLapTime'] / stints['SmallestCumulativeLapTime']

    stints.reset_index()

    fig, ax = plt.subplots()

    for driver in drivers:
        driver_stint = stints.loc[stints['Driver'] == driver].reset_index()
        
        try:
            driver_color = fastf1.plotting.driver_color(driver)
        except KeyError:
            driver_color = '#1e3d61'  
            
        ax.plot(driver_stint["LapNumber"],
                driver_stint["IntervalToLeader"],
                color=driver_color,
                label=driver
            )

    ax.set_title(f'{SESSION} GP - {drivers[0]} vs {drivers[1]}')
    ax.set_xlabel('Lap Number')
    ax.set_ylabel(f'{drivers[0]} vs. {drivers[1]} (s)')
    plt.grid(color='#C0C0C0', which='both', axis='both')

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.savefig(f'graphs/{YEAR}/{YEAR} {SESSION} GP - {drivers[0]} Laptimes To {drivers[1]}.png', format='png' )