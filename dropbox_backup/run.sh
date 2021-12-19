#!/bin/bash

CONFIG_PATH=/data/options.json

# Dropbox authentication token
TOKEN=$(jq --raw-output ".oauth_access_token" $CONFIG_PATH)

# Configuration
OUTPUT_DIR=$(jq --raw-output ".output // empty" $CONFIG_PATH)
KEEP_LAST=$(jq --raw-output ".keep_last // empty" $CONFIG_PATH)

if [[ -z "$OUTPUT_DIR" ]]; then
    OUTPUT_DIR="/"
fi

echo "[Info] Files will be uploaded to: ${OUTPUT_DIR}"
echo "[Info] Listening for messages via stdin service call..."

# listen for input
while read -r msg; do
    # parse JSON
    echo "$msg"
    cmd="$(echo "$msg" | jq --raw-output '.command')"
    echo "[Info] Received message with command ${cmd}"
    if [[ $cmd = "upload" ]]; then

        # Upload files
        echo "[Info] Uploading all .tar files in /backup"
        python3 /upload.py "$TOKEN" "$OUTPUT_DIR"

        # Remove stale backups
        if [[ "$KEEP_LAST" ]]; then
            echo "[Info] keep_last option is set, cleaning up files..."
            python3 /keep_last.py "$KEEP_LAST"
        fi

    else
        # received undefined command
        echo "[Error] Command not found: ${cmd}"
    fi

done
