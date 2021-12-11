import argparse
import os

import requests
from dateutil.parser import parse
import pytz

BASE_URL = "http://hassio/"


# Get the hassio token for authentication.
def get_headers():
    return {"X-HASSIO-KEY": os.environ.get("HASSIO_TOKEN")}


# If a naive (not timezone aware) datetime is found set it to UTC
def dates_to_utc(backups):

    for backup in backups:
        d = parse(backup["date"])

        if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:

            print("[INFO] Naive DateTime found for backup {}, setting to UTC...".
                  format(backup["name"]))
            backup["date"] = d.replace(tzinfo=pytz.utc).isoformat()

    return (backups)


# Return stale backups
def stale_only(backups, number_to_keep):

    backups.sort(key=lambda item: parse(item["date"]), reverse=True)
    keepers = backups[:number_to_keep]
    stale_backups = [snap for snap in backups if snap not in keepers]

    return stale_backups


# Delete backups
def delete_backup(stale_backups, headers):

    for backup in stale_backups:

sests.post(
            BASE_URL + "snapshots/" + backup["slug"] + "/remove",
            headers=headers)

        # Print message based on response.
        if res.ok:
            print("[Info] Deleted backup {}".format(backup["name"]))
            continue

        else:
            # log an error
            print("[Error] Failed to delete backup {}: {}".format(
                backup["name"], res.status_code))


def main(number_to_keep):

    my_headers = get_headers()

    # Get backup name and information as a list of dicts.
    backup_info = requests.get(BASE_URL + "backups", headers=my_headers)
    backup_info.raise_for_status()
    backups = backup_info.json()["data"]["backups"]

    # Set all dates to UTC
    backups = dates_to_utc(backups)

    # Sort by date and make list of backups to delete
    stale_backups = stale_only(backups, number_to_keep)

    # Delete all stale backups
    delete_backup(stale_backups, my_headers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove old hassio backups.")
    parser.add_argument("number", type=int, help="Number of backups to keep.")
    args = parser.parse_args()
    main(args.number)
