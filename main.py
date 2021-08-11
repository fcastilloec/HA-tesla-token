#!/usr/bin/env python3
import json
import os
from sys import exit

# Buffer for not triggering a tesla token update from HA
buffer = 604800  # 1 week in seconds

if os.environ.get("PYTHON_ENV") == "production":
    ha_entries = "/usr/share/hassio/homeassistant/.storage/core.config_entries"
    tesla_token = "/home/felipe/.config/transmission/tokens/tesla.json"
else:
    ha_entries = os.path.join(os.getcwd(), "core.config_entries")
    tesla_file = os.path.join(os.getcwd(), "tesla.json")

# Read JSON file
with open(ha_entries) as file:
    data_entries = json.load(file)

# Read Tesla token
with open(tesla_file) as file:
    tesla_token = json.load(file)

# Find index of Tesla entry
for index, entry in enumerate(data_entries["data"]["entries"]):
    if entry["domain"] == "tesla":
        tesla_index = index
        break
else:
    tesla_index = False

# Modify JSON if Tesla entry exists
if tesla_index:
    data_entries["data"]["entries"][tesla_index]["data"]["token"] = ""
    data_entries["data"]["entries"][tesla_index]["data"]["access_token"] = tesla_token["access_token"]
    data_entries["data"]["entries"][tesla_index]["data"]["expiration"] = (
        tesla_token["created_at"] + tesla_token["expires_in"] + buffer
    )
else:
    print("No Tesla entry found in HA")
    exit(1)

# Write modified entry file
with open(ha_entries, "w") as file:
    json.dump(data_entries, file, indent=4)
