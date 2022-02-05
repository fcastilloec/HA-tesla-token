#!/usr/bin/env python3
""" Checks for updated Tesla tokens """

import json
import logging
import os
import sys

# Change to DEBUG is needed
logging.basicConfig(level=logging.WARNING)

if os.environ.get("PYTHON_ENV") == "production":
    logging.debug("Running in PRODUCTION mode")
    HA_ENTRIES = "/usr/share/hassio/homeassistant/.storage/core.config_entries"
    TESLA_FILE = "/home/felipe/.config/ifttt-server/tokens/tesla.json"
else:
    logging.debug("Running in DEVELOPER mode")
    HA_ENTRIES = os.path.join(os.getcwd(), "core.config_entries")
    TESLA_FILE = os.path.join(os.getcwd(), "tesla.json")

# Read HA config file
with open(HA_ENTRIES, encoding="utf-8") as file:
    data_entries = json.load(file)
    # Find index of Tesla entry
    for index, entry in enumerate(data_entries["data"]["entries"]):
        if entry["domain"] == "tesla_custom":
            tesla_index = index
            break
    else:
        logging.error("No Tesla domain found!")
        sys.exit(1)

# Read Tesla token file
with open(TESLA_FILE, mode="r+", encoding="utf-8") as file:
    if sorted(json.load(file).items()) == sorted(data_entries["data"]["entries"][tesla_index]["data"].items()):
        print("Not need to update")
        sys.exit(0)
    else:
        print("Updating tokens")
        # Write modified entry file
        file.seek(0)
        json.dump(data_entries["data"]["entries"][tesla_index]["data"], file, indent=2)
        file.write("\n")
        file.truncate()
