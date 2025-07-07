import requests
import argparse
import re
import json


parser = argparse.ArgumentParser(description='Compare two trip reports')
parser.add_argument('first_url', type=str, help='URL of the 1st tripreport')
parser.add_argument('second_url', type=str, help='URL of the 2nd tripreport')
args = parser.parse_args()


def get_info_from_trip_report(trip_report_id, person_id):
    list_species_url = f'https://ebird.org/tripreport-internal/v1/taxon-list/{trip_report_id}?' \
                       f'tripReportPersonId={person_id}'
    response = requests.get(list_species_url)
    list_species = set()
    for species in response.json():
        list_species.add(species['commonName'])
    return list_species


splitted_url = args.first_url.split('/')
first_person_id = int(splitted_url[-1])
trip_report_id = splitted_url[-2]

splitted_url = args.second_url.split('/')
second_person_id = int(splitted_url[-1])

if splitted_url[-2] != trip_report_id:
    raise ValueError('Not the same trip report')

# Getting names
birders = dict()
birders[first_person_id] = 'PERSON1'
birders[second_person_id] = 'PERSON2'

trip_report_url = f'https://ebird.org/tripreport/{trip_report_id}'
response = requests.get(trip_report_url)
match = re.search(r'var\s+tripReport\s*=\s*({.*?});', response.text, re.DOTALL)

if match:
    js_object = match.group(1)
    trip_report_info = json.loads(js_object)
    for people in trip_report_info['people']:
        birders[people['tripReportPersonId']] = people['userDisplayName']
else:
    print('NO MATCH (TRIP REPORT IS LIMITED?)')

list_species1 = get_info_from_trip_report(trip_report_id, first_person_id)
list_species2 = get_info_from_trip_report(trip_report_id, second_person_id)

print(f'TOTAL SPECIES FOR {birders[first_person_id]} :', len(list_species1))
print(f'ONLY FOR {birders[first_person_id]} :', list_species1 - list_species2)
print(' ')
print(f'TOTAL SPECIES FOR {birders[second_person_id]} :', len(list_species2))
print(f'ONLY FOR {birders[second_person_id]} :', list_species2 - list_species1)
