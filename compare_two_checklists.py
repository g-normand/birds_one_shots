import requests
import argparse
import re
import json


parser = argparse.ArgumentParser(description='Compare two trip reports')
parser.add_argument('first_url', type=str, help='URL of the 1st tripreport')
parser.add_argument('second_url', type=str, help='URL of the 2nd tripreport')
args = parser.parse_args()

headers = dict()
headers['X-eBirdApiToken'] = open('.ebird_key').read().strip()


common_names = dict()
common_names['brvear1'] = 'Brown Violetear'
common_names['spehum1'] = 'Speckled Hummingbird'
common_names['lotsyl1'] = 'Long-tailed Sylph'
common_names['broinc1'] = 'Bronzy Inca'
common_names['colinc1'] = 'Collared Inca'
common_names['chbcor1'] = 'Chestnut-breasted Coronet'
common_names['boorat2'] = 'Peruvian Racket-tail'
common_names['whthil3'] = 'Green-backed Hillstar'
common_names['fabbri1'] = 'Fawn-breasted Brilliant'
common_names['vifbri1'] = 'Violet-fronted Brilliant'
common_names['gorwoo2'] = 'Gorgeted Woodstar'
common_names['ruboro1'] = 'Russet-backed Oropendola'
common_names['scrcac1'] = 'Scarlet-rumped Cacique'
common_names['paltan1'] = 'Palm Tanager'
common_names['banana'] = 'Bananaquit'
common_names['spvear1'] = 'Sparkling Violetear'
common_names['cinfly2'] = 'Cinnamon Flycatcher'
common_names['grnjay'] = 'Green Jay'
common_names['bawswa1'] = 'Blue-and-white Swallow'
common_names['rucspa1'] = 'Rufous-collard Sparrow'
common_names['scrcac4'] = 'Scarlet-rumped Cacique (Subtropical)'


def get_info_from_checklist(url):
    subId = url.split('/')[-1]
    list_species_url = f'https://api.ebird.org/v2/product/checklist/view/{subId}'
    response = requests.get(list_species_url, headers=headers)

    user_name = response.json()['userDisplayName']
    list_species = set()
    for species in response.json()['obs']:
        name = common_names[species['speciesCode']] if species['speciesCode'] in common_names else \
            species['speciesCode']
        list_species.add(name)
    return user_name, list_species


birders1, list_species1 = get_info_from_checklist(args.first_url)
birders2, list_species2 = get_info_from_checklist(args.second_url)

print(f'TOTAL SPECIES FOR {birders1} :', len(list_species1))
print(f'ONLY FOR {birders1} :', list_species1 - list_species2)
print(' ')
print(f'TOTAL SPECIES FOR {birders2} :', len(list_species2))
print(f'ONLY FOR {birders2} :', list_species2 - list_species1)
