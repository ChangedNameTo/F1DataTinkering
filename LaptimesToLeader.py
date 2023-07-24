import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

def generate_laptimes_graphs(race, year, session, filter_np=False, filter_dnf=False):
    driver_laps = race.laps.reset_index()
   
    TITLE_0 = f'{year} {session} GP - Interval to Leader'  
    TITLE_1 = f'{year} {session} GP - Norm. Interval to Leader'  
    
    # Filter non-point finishers
    if filter_np:
        TITLE_0 = f'{year} {session} GP - Interval to Leader (Top 10)'  
        TITLE_1 = f'{year} {session} GP - Norm. Interval to Leader (Top 10)'  
        
        point_finishers = race.drivers[10:]
        driver_laps = driver_laps[~driver_laps['DriverNumber'].isin(point_finishers)]

    # Filter non finishers
    if filter_dnf:
        TITLE_0 = f'{year} {session} GP - Interval to Leader (Finished)'  
        TITLE_1 = f'{year} {session} GP - Norm. Interval to Leader (Finished)'  
        
        retired_drivers = race.results.loc[race.results['ClassifiedPosition'].isin(['R', 'D', 'E', 'W', 'F', 'N'])]['Abbreviation']
        driver_laps = driver_laps[~driver_laps['Driver'].isin(retired_drivers)]

    drivers = pd.unique(driver_laps['Driver'])

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

    stints.to_csv('output.csv')

    fig, ax = plt.subplots(ncols=2,figsize=(32,16))

    for driver in drivers:
        driver_stint = stints.loc[stints['Driver'] == driver].reset_index()
        
        try:
            driver_color = fastf1.plotting.driver_color(driver)
        except KeyError:
            driver_color = '#1e3d61'  
            
        ax[0].plot(driver_stint["LapNumber"],
                driver_stint["IntervalToLeader"],
                color=driver_color,
                label=driver
            )

    ax[0].set_title(TITLE_0)
    
    ax[0].set_xlabel('Lap Number')
    ax[0].set_ylabel('Interval to Leader (s)')
    ax[0].margins(0.05, 0.1)
    ax[0].legend()

    for driver in drivers:
        driver_stint = stints.loc[stints['Driver'] == driver].reset_index()
        
        try:
            driver_color = fastf1.plotting.driver_color(driver)
        except KeyError:
            driver_color = '#1e3d61'  
        
        plt.plot(driver_stint["LapNumber"],
                driver_stint["NormalizedIntervalToLeader"],
                color=driver_color,
                label=driver
            )

    ax[1].set_title(TITLE_1)
    ax[1].set_xlabel('Lap Number')
    ax[1].set_ylabel('Normalized Interval to Leader')
    ax[1].margins(0.05, 0.1)
    ax[1].legend()

    plt.savefig(f'graphs/{year}/{TITLE_0}.png', format='png') 