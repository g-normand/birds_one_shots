import csv
import os
import requests
import imagehash
from io import BytesIO
from urllib.parse import urlparse
import argparse
from PIL import Image


parser = argparse.ArgumentParser(description='inat create CSV')
parser.add_argument('year', type=str, help='Year to check')
args = parser.parse_args()

YEAR = args.year
USER_ID = "gnormand"
CSV_FILE = f"inat_files/inat_images_{YEAR}.csv"
LOCAL_FOLDER = os.path.expanduser(f"~/Dropbox/photos_animaux/unconfirmed/{YEAR}")
PHASH_THRESHOLD = 10 


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

def get_all_photo_hashes(observations):
    hashes = []
    for o in observations:
        for ph in o.get("photos", []):
            # choose medium size
            url = ph["url"].replace("square", "medium")
            try:
                img = Image.open(BytesIO(requests.get(url, timeout=20).content))
                hashes.append((o["id"], imagehash.phash(img)))
            except Exception as e:
                print("Error downloading", url, e)
    return hashes

def local_hashes(folder):
    res = []
    for fname in os.listdir(folder):
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, fname)
            try:
                h = imagehash.phash(Image.open(path))
                res.append((fname, h))
            except Exception as e:
                print("Error hashing", path, e)
    return res

def load_existing_csv(path):
    """Load existing CSV as a dictionary keyed by obs_id."""
    if not os.path.exists(path):
        return {}

    existing = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing[row["obs_id"]] = row
    return existing


def compare(local, remote_hashes):
    present = {}
    for fname, lh in local:
        for obs_id, rh in remote_hashes:
            if lh - rh < PHASH_THRESHOLD:
                present[str(obs_id)] = fname
                break        
    return present

def save_csv(path, rows):
    """Save CSV rows to file."""
    fieldnames = ["obs_id", "local_filename"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    print("📂 Loading existing CSV...")
    existing = load_existing_csv(CSV_FILE)
    if len(existing) > 0:
        print("CSV already created. Exited")
        return

    print("📡 Fetching iNaturalist observations...")
    obs_list = api_fetch_needs_id(USER_ID)
    print(f"🔎 Found {len(obs_list)} observations with needs_id.")

    print("Downloading & hashing photos from iNaturalist ...")
    remote = get_all_photo_hashes(obs_list)
    print("Got", len(remote), "remote photos.")

    print("Hashing local photos ...")
    local = local_hashes(LOCAL_FOLDER)
    print("Comparing ...")
    result = compare(local, remote)
    
    updated_rows = dict()
    for obs in obs_list:
        obs_id = str(obs["id"])
        photos = obs.get("photos", [])
        if not photos:
            continue  # skip obs with no photos

        updated_rows[obs_id] = {
            "obs_id": obs_id,
            "local_filename": result[obs_id] if obs_id in result else '',
        }


    # Save CSV
    print("💾 Saving CSV...")
    save_csv(CSV_FILE, updated_rows.values())

    print("✅ Done!\n")



if __name__ == "__main__":
    main()

