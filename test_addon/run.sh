#!/bin/bash

CONFIG_PATH=/data/options.json

# Authentication keys
APP_KEY=$(jq --raw-output ".oauth_app_key" $CONFIG_PATH)
APP_SECRET=$(jq --raw-output ".oauth_app_secret" $CONFIG_PATH)

# Configuration
OUTPUT_DIR=$(jq --raw-output ".output // empty" $CONFIG_PATH)
KEEP_LAST=$(jq --raw-output ".keep_last // empty" $CONFIG_PATH)
FILETYPES=$(jq --raw-output ".filetypes // empty" $CONFIG_PATH)

if [[ -z "$OUTPUT_DIR" ]]; then
    OUTPUT_DIR="/"
fi

echo "[Info] Files will be uploaded to: ${OUTPUT_DIR}"

echo "[Info] Saving OAUTH_APP_KEY to /etc/uploader.conf"
echo "OAUTH_APP_KEY=${APP_KEY}" >> /etc/uploader.conf

echo "[Info] Saving OAUTH_APP_SECRET to /etc/uploader.conf"
echo "OAUTH_APP_SECRET=${APP_SECRET}" >> /etc/uploader.conf

echo "[Info] Listening for messages via stdin service call..."

# listen for input
while read -r msg; do
    # parse JSON
    echo "$msg"
    cmd="$(echo "$msg" | jq --raw-output '.command')"
    echo "[Info] Received message with command ${cmd}"
    if [[ $cmd = "upload" ]]; then
        echo "[Info] Uploading all .tar files in /backup (skipping those already in Dropbox)"
        ./dropbox_uploader.sh -s -f /etc/uploader.conf upload /backup/*.tar "$OUTPUT_DIR"
        if [[ "$KEEP_LAST" ]]; then
            echo "[Info] keep_last option is set, cleaning up files..."
            python3 /keep_last.py "$KEEP_LAST"
        fi
        if [[ "$FILETYPES" ]]; then
            echo "[Info] filetypes option is set, scanning share directory for files with extensions ${FILETYPES}"
            find /share -regextype posix-extended -regex "^.*\.(${FILETYPES})" -exec ./dropbox_uploader.sh -s -f /etc/uploader.conf upload {} "$OUTPUT_DIR" \;
        fi
    else
        # received undefined command
        echo "[Error] Command not found: ${cmd}"
    fi
done
