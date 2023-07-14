import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

SESSION = 'British'
YEAR = 2023

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

race = fastf1.get_session(YEAR, SESSION, 'R')
race.load()

driver_laps = race.laps.pick_quicklaps().reset_index()
drivers = pd.unique(race.laps['Driver'])

stints = driver_laps[["Driver", "Stint", "Compound", "LapNumber", "LapTime", "TyreLife"]]
stints['FullName'] = stints['Driver'].map(fastf1.plotting.DRIVER_TRANSLATE)
stints['Color'] = stints['FullName'].map(fastf1.plotting.DRIVER_COLORS)
stints.reset_index(drop=True)

for compound in ['HARD', 'MEDIUM', 'SOFT', 'INTER', 'WET']:
    fig, ax = plt.subplots()
    sns.scatterplot(data=stints.loc[stints['Compound'] == compound].reset_index(),
                x="TyreLife",
                y="LapTime",
                ax=ax,
                hue="FullName",
                palette=fastf1.plotting.DRIVER_COLORS,
                legend='auto')

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    leg = ax.get_legend()

    ax.set_title(f'{SESSION} GP - {compound} Tire')
    ax.set_xlabel('Stint Length')
    ax.set_ylabel('Lap Time')
    ax.invert_yaxis()

    ax.margins(0.05, 0.1)

    plt.grid(color='w', which='both', axis='both')
    sns.despine(left=True, bottom=True)

    plt.savefig(f'graphs/{YEAR}/{YEAR} {SESSION} GP - {compound} TYRE.png', format='png', bbox_extra_artists=(leg,), bbox_inches='tight')
