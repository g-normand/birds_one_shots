import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Get bigday missing birds')
parser.add_argument('region', type=str)
args = parser.parse_args()

region = args.region

list_info = dict()
list_info['big_day'] = f'https://ebird.org/region/{region}/bird-list?yr=BIGDAY_2024b&rank=lrec&hs_sortBy=taxon_order&hs_o=asc'
list_info['current_year'] = f'https://ebird.org/region/{region}/bird-list?hs_sortBy=taxon_order&hs_o=asc'

list_birds = dict()

for type_list in list_info:
    list_birds[type_list] = set()
    response = requests.get(list_info[type_list])
    soup = BeautifulSoup(response.text, 'html.parser')
    species_common_spans = soup.find('section', {'aria-labelledby': 'nativeNaturalized'}).\
        find_all('span', class_='Species-common')
    # Extract and print the text inside each <span>
    for span in species_common_spans:
        list_birds[type_list].add(span.text)


print('ONLY IN BIG DAY', list_birds['big_day'] - list_birds['current_year'])
print('NOT IN BIG DAY', list_birds['current_year'] - list_birds['big_day'])
