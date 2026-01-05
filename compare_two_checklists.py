import requests
import argparse
import re
import json
import csv


common_names = {}
with open("species.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=",")
    for row in reader:
        common_names[row["code"]] = row["species"]

parser = argparse.ArgumentParser(description='Compare two trip reports')
parser.add_argument('first_url', type=str, help='URL of the 1st tripreport')
parser.add_argument('second_url', type=str, help='URL of the 2nd tripreport')
args = parser.parse_args()

headers = dict()
headers['X-eBirdApiToken'] = open('.ebird_key').read().strip()



def get_info_from_checklist(url):
    subId = url.split('/')[-1]
    list_species_url = f'https://api.ebird.org/v2/product/checklist/view/{subId}'
    response = requests.get(list_species_url, headers=headers)

    user_name = response.json()['userDisplayName']
    list_species = set()
    for species in response.json()['obs']:
        if species['speciesCode'] in common_names:
            name = common_names[species['speciesCode']].split(' (')[0]
        else:
            #print(f"VERIFY : https://ebird.org/species/{species['speciesCode']}")
            print(f"{species['speciesCode']},??")
            name = species['speciesCode']
        list_species.add(name)
    return user_name, list_species


birders1, list_species1 = get_info_from_checklist(args.first_url)
birders2, list_species2 = get_info_from_checklist(args.second_url)

print(f'TOTAL SPECIES FOR {birders1} :', len(list_species1))
print(f'ONLY FOR {birders1} :', list_species1 - list_species2)
print(' ')
print(f'TOTAL SPECIES FOR {birders2} :', len(list_species2))
print(f'ONLY FOR {birders2} :', list_species2 - list_species1)
