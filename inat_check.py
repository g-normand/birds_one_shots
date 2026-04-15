import os
import csv
import requests
import argparse


parser = argparse.ArgumentParser(description='Check inat obs')
parser.add_argument('year', type=str, help='Year to check')
args = parser.parse_args()

YEAR = args.year
USER_ID = "gnormand"
LOCAL_FOLDER = os.path.expanduser(f"~/Dropbox/photos_animaux/unconfirmed/{YEAR}")
CSV_FILE = f"inat_files/inat_images_{YEAR}.csv"


def api_fetch_needs_id(username):
    """Fetches all observations with quality_grade=needs_id for the user."""
    url = "https://api.inaturalist.org/v1/observations"
    obs = []
    params = {
        "user_id": username,
        "quality_grade": "needs_id",
        "page": 1,
        "d1": f"{YEAR}/01/01",
        "d2": f"{YEAR}/12/31",
        "per_page": 200
    }
    while True:
        resp = requests.get(url, params=params).json()
        results = resp.get("results", [])
        if not results:
            break
        obs.extend(results)
        params["page"] += 1
    return obs


def get_csv_infos(path):
    existing_names = {}
    existing_ids = {}
    csv_set = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_names[row["local_filename"]] = row
            existing_ids[row["obs_id"]] = row
            csv_set.add(str(row['obs_id']))
    return existing_names, existing_ids, csv_set
    
def main():
    print("📡 Fetching iNaturalist observations...")
    obs_list = api_fetch_needs_id(USER_ID)
    print(f"🔎 Found {len(obs_list)} observations with needs_id for the year {YEAR}.")

    existing_names, existing_ids, csv_set = get_csv_infos(CSV_FILE)
    inat_set = set()

    for obs in obs_list:
        obs_id = str(obs["id"])
        inat_set.add(obs_id)

    nb_obs_csv = 0       
    for obs_id in csv_set - inat_set:
        nb_obs_csv += 1
        if nb_obs_csv == 1:
            print(f'IN CSV, NOT IN INAT :')
        print(existing_ids[obs_id])

    if nb_obs_csv > 0:
        print('USE : ')
        print('')
        print(f'gedit inat_files/inat_images_{YEAR}.csv')
        print('')
        print('_____')

    nb_obs_local = 0
    for fname in os.listdir(LOCAL_FOLDER):
       if fname not in existing_names:
            nb_obs_local += 1
            if nb_obs_local == 1:
                print('Files in directory but not in the CSV : ')
            print(fname)
    
    if nb_obs_local > 0:
        print('_____')
    elif nb_obs_csv == 0:
        print('TUDO BEEEEM!')       
       
 
if __name__ == "__main__":
    main()

