import fastf1

from LaptimesToLeader import generate_laptimes_graphs
from LaptimeComp import generate_laptime_comp

SESSION = 'HUNGARIAN'
YEAR = 2023

DRIVER_PAIRINGS = {
    'MER':['HAM', 'RUS'],
    'RBR':['VER', 'PER'],
    'FER':['SAI', 'LEC'],
    'HAA':['HUL', 'MAG'],
    'AMR':['ALO', 'STR'],
    'APN':['GAS', 'OCO'],
    'APT':['RIC', 'TSU'],
    'ARR':['BOT', 'ZHO'],
    'WIL':['ALB', 'SAR'],
    'MCL':['NOR', 'PIA']
}

race = fastf1.get_session(YEAR, SESSION, 'R')
race.load()

race.laps.to_csv(f'data/{YEAR}/{YEAR} {SESSION} Lap Data.csv')

# Full Graph
generate_laptimes_graphs(race, YEAR, SESSION)
# Filtered Non-points
generate_laptimes_graphs(race, YEAR, SESSION, True)
# Filtered DNF
generate_laptimes_graphs(race, YEAR, SESSION, False, True)

for index, driver_pairing in enumerate(DRIVER_PAIRINGS):
    driver_pair = DRIVER_PAIRINGS[driver_pairing]
    generate_laptime_comp(race, YEAR, SESSION, driver_pair)