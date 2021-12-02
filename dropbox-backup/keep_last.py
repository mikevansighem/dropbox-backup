import argparse
import os

import requests
from dateutil.parser import parse
import pytz

BASE_URL = "http://hassio/"
HEADERS = {"X-HASSIO-KEY": os.environ.get("HASSIO_TOKEN")}

def dates_to_utc(backups):
    """ Convert dates in the list of backups to UTC. """

    for backup in backups:
        d = parse(backup["date"])
        if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
            print("Naive DateTime found for backup {}, setting to UTC...".
                  format(backup["slug"]))
            backup["date"] = d.replace(tzinfo=pytz.utc).isoformat()

    return (backups)


def main(number_to_keep):

    # Get backup name and information as a list of dicts
    backup_info = requests.get(BASE_URL + "backups", headers=HEADERS)
    backup_info.raise_for_status()
    backups = backup_info.json()["data"]["backups"]

    # Set all dates to UTC
    backups = dates_to_utc(backups)

    # Sort by date and make list of backups to delete
    backups.sort(key=lambda item: parse(item["date"]), reverse=True)
    keepers = backups[:number_to_keep]
    stale_backups = [snap for snap in backups if snap not in keepers]

    # Delete all stale backups
    for backup in stale_backups:
        # call hassio API deletion
        res = requests.post(
            BASE_URL + "backups/" + backup["slug"] + "/remove",
            headers=HEADERS)
        if res.ok:
            print("[Info] Deleted backup {}".format(backup["slug"]))
            continue
        else:
            # log an error
            print("[Error] Failed to delete backup {}: {}".format(
                backup["slug"], res.status_code))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove old hassio backups.")
    parser.add_argument("number", type=int, help="Number of backups to keep.")
    args = parser.parse_args()
    main(args.number)
