# Hass.io Add-on: Dropbox Sync

Back up your Hass.io snapshots to Dropbox.

[![Last commit](https://img.shields.io/github/last-commit/mikevansighem/test_addon?style=flat-square)](https://github.com/mikevansighem/test_addon/commits/master)
[![Commits per month](https://img.shields.io/github/commit-activity/m/mikevansighem/test_addon?style=flat-square)](https://github.com/mikevansighem/test_addon/commits/master)
[![License](https://img.shields.io/github/license/mikevansighem/test_addon?style=flat-square)](https://github.com/mikevansighem/test_addon/blob/master/LICENSE)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/mikevansighem/test_addon/CI?style=flat-square)](https://github.com/mikevansighem/test_addon/actions)
[![GitHub issues](https://img.shields.io/github/issues-raw/mikevansighem/test_addon?style=flat-square)](https://github.com/mikevansighem/test_addon/issues)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/mikevansighem/test_addon?style=flat-square)](https://github.com/mikevansighem/test_addon/releases)

## :page_facing_up: About

This add-on allows you to upload your Hass.io snapshots to your Dropbox,
keeping your snapshots safe and available in case of hardware failure. Uploads
are triggered via a service call, making it easy to automate periodic backups
or trigger uploads to Dropbox via script as you would with any other Home
Assistant service.

This add-on uses the [Dropbox-Uploader](https://github.com/andreafabrizi/Dropbox-Uploader)
bash script to upload files to Dropbox. It requires that you generate an access
token via the Dropbox Web UI, which must be added to this add-on's
configuration via the Hass.io UI (see below for further details).

## Installation

1. Add this repository to your Hass.io instance: `https://github.com/mikevansighem/dropbox_sync`.
2. Install the Dropbox Sync add-on.
3. Configure the add-on with your Dropbox OAuth Token and desired output
directory (see configuration below).

## Configuration

To access your personal Dropbox, this add-on requires an access token.
Follow these steps to create an Access Token:

1. Go to [Your Dropbox apps](https://www.dropbox.com/developers/apps).
2. Click the "Create App" button.
3. Follow the prompts to set permissions and choose a unique name for your "app" token.

Once you have created the token, copy it into this add-on's configuration under
the `oauth_access_token` label.

|Parameter|Required|Description|
|---------|--------|-----------|
|`oauth_access_token`|Yes|The "app" access token you generated above via the Dropbox UI.|
|`output`|Yes|The target directory in your Dropbox to which you want to upload. If left empty, defaults to `/`, which represents the top level of directory of your Dropbox.|
|`keep_last`|Yes|If set, the number of snapshots to keep locally. If there are more than this number of snapshots stored locally, the older snapshots will be deleted from local storage after being uploaded to Dropbox. If not set, no snapshots are deleted from local storage.|
|`filetypes`|Yes|File extensions of files to upload from `/share` directory, seperated by <code>&#124;</code> (ex: `"jpg|png" or "png"`).|

Example Configuration:

```yaml
{
  oauth_access_token: "<YOUR_TOKEN>"
  output: "/hasssio-backups/"
  keep_last: 2
  filetypes: "tag|zip"
}
```

## Usage

Dropbox Sync uploads all snapshot files (specifically, all `.tar` files) in the
Hass.io `/backup` directory to a specified path in your Dropbox. This target
path is specified via the `output`option. Once the add-on is started, it is
listening for service calls.

After the add-on is configured and started, trigger an upload by calling the
`hassio.addon_stdin` service with the following service data:

```yaml
service: hassio.addon_stdin
data:
  addon: 7be23ff5_dropbox_sync
  input:
    command: upload

```

This triggers the `dropbox_uploader.sh` script with the provided access token.
You can use Home Assistant automations or scripts to run uploads at certain
time intervals, under certain conditions, etc.

Dropbox Sync will only upload new snapshots to the specified path, and will
skip snapshots already in the target Dropbox path.

The `keep last` option allows the add-on to clean up the local backup
directory, deleting the local copies of the snapshots after they have been
uploaded to Dropbox. If `keep_last` is set to some integer `x`, only the latest
`x` snapshots will be stored locally; all other (older) snapshots will
be deleted from local storage. All snapshots are always uploaded to Dropbox,
regardless of this option.

The `filetypes` option allows the add-on to upload arbitrary filetypes from the
Hass.io `/share`directory to Dropbox. Set this option to a string of extensions
seperated by `|` to upload matching files to Dropbox. For example, setting this
option to `"jpg|png"` will upload all files in the `/share` folder ending in
`.jpg` or `.png`. These files will be uploaded to the directory
specified by the `output` option.
