# Notes

 1) Open the following URL in your Browser, and log in using your account: https://www.dropbox.com/developers/apps
 2) Click on "Create App", then select "Choose an API: Scoped Access"
 3) "Choose the type of access you need: App folder"
 4) Enter the "App Name" that you prefer (e.g. MyUploader42332445026208), must be unique
 Now, click on the "Create App" button.
 5) Now the new configuration is opened, switch to tab "permissions" and check "files.metadata.read/write" and "files.content.read/write"
 Now, click on the "Submit" button.
 6) Now to tab "settings" and provide the following information:



    echo -ne " App key: "
    read -r OAUTH_APP_KEY

    echo -ne " App secret: "
    read -r OAUTH_APP_SECRET


    $CURL_BIN $CURL_ACCEPT_CERTIFICATES $API_OAUTH_TOKEN -d code=$access_code -d grant_type=authorization_code -u $OAUTH_APP_KEY:$OAUTH_APP_SECRET -o "$RESPONSE_FILE" 2>/dev/null
    check_http_response
    OAUTH_REFRESH_TOKEN=$(sed -n 's/.*"refresh_token": "\([^"]*\).*/\1/p' "$RESPONSE_FILE")
    echo "CONFIGFILE_VERSION=2.0" > "$CONFIG_FILE"
    echo "OAUTH_APP_KEY=$OAUTH_APP_KEY" >> "$CONFIG_FILE"
    echo "OAUTH_APP_SECRET=$OAUTH_APP_SECRET" >> "$CONFIG_FILE"
    echo "OAUTH_REFRESH_TOKEN=$OAUTH_REFRESH_TOKEN" >> "$CONFIG_FILE"
    echo "   The configuration has been saved."
