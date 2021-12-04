# Home Assistant add-on: Dropbox backup

[![Last commit](https://img.shields.io/github/last-commit/mikevansighem/dropbox-backup?style=flat-square)](https://github.com/mikevansighem/dropbox-backup/commits/main)
[![Commits per month](https://img.shields.io/github/commit-activity/m/mikevansighem/dropbox-backup?style=flat-square)](https://github.com/mikevansighem/dropbox-backup/commits/main)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](https://github.com/mikevansighem/dropbox-backup/blob/main/LICENSE.md)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/mikevansighem/dropbox-backup/CI?style=flat-square)](https://github.com/mikevansighem/dropbox-backup/actions)
[![GitHub issues](https://img.shields.io/github/issues-raw/mikevansighem/dropbox-backup?style=flat-square)](https://github.com/mikevansighem/dropbox-backup/issues)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/mikevansighem/dropbox-backup?style=flat-square)](https://github.com/mikevansighem/dropbox-backup/releases)

![Supports armhf Architecture](https://img.shields.io/badge/armhf-yes-green?style=flat-square)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-yes-green?style=flat-square)
![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green?style=flat-square)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green?style=flat-square)
![Supports i386 Architecture](https://img.shields.io/badge/i386-yes-green?style=flat-square)

Upload your Home Assistant backups to Dropbox.

## :page_facing_up: About

This add-on allows you to upload your Home Assistant backups to your Dropbox,
keeping your backups safe and available in case of hardware failure. Uploads
are triggered via a service call, making it easy to automate periodic backups
or trigger uploads to Dropbox via script as you would with any other Home
Assistant service.

This add-on is heavily based on [Dropbox Sync](https://github.com/danielwelch/hassio-dropbox-sync)
from [Daniel Welch](https://github.com/danielwelch). Major thanks for his
initial work!

The add-on uses the [Dropbox-Uploader](https://github.com/andreafabrizi/Dropbox-Uploader)
bash script to upload files to Dropbox. It requires that you generate an access
token via the Dropbox Web UI, which must be added to this add-on's
configuration via the Home Assistant UI (see below for further details).

## ⤵️ Installation

1. Go to the Supervisor add-on store in Home Assistant.
1. Click on the "three-dots-menu" and choose `Repositories`.
1. Add this repository to your Home Assistant instance: `https://github.com/mikevansighem/dropbox_sync`.
1. Install the Dropbox backup add-on.
1. Configure the add-on with your Dropbox OAuth Token and desired output directory (see configuration below).

## 🏗 Configuration

### Generate Dropbox access token

To access your personal Dropbox, this add-on requires an access token.
Follow these steps to create an access token:

1. Go to [Your Dropbox apps](https://www.dropbox.com/developers/apps).
1. Click on `Create App`.
1. Select `Scoped Access` and choose between full or app folder only access.
1. Give your app a unique name and click on `Create App`.
1. Now your app is created go to the permissions tab and tick `files.metadata.write`.
1. Back on the settings tab, go to "Generated access token" and click `Generate`.
1. Copy the access code for use in your configuration.

### Setup the add-on

Once you have created the token, copy it into this add-on's configuration under
the `oauth_access_token` label.

<!-- markdownlint-disable MD033 -->

|Parameter|Required|Description|
|---------|--------|-----------|
|`oauth_access_token`|Yes|The "app" access token you generated above via the Dropbox UI.|
|`output`|Yes|The target directory in Dropbox to which you want to upload. If left empty, defaults to `/`, which represents the top level of directory of your Dropbox.|
|`keep_last`|No|If set, the number of backups to keep locally. If there are more than this number of backups stored locally, the older backups will be deleted from local storage after being uploaded to Dropbox. If not set, no backups are deleted from local storage.|
|`filetypes`|No|File extensions of files to upload from `/share` directory, seperated by <code>&#124;</code> (eg: <code>"jpg&#124;png"</code> or `"png"`).|

<!-- markdownlint-enable MD033 -->

Example configuration:

```yaml
{
  oauth_access_token: "<YOUR_TOKEN>"
  output: "/hasssio-backups/"
  keep_last: 2
  filetypes: "tag|zip"
}
```

## 🚀 Usage

Dropbox Sync uploads all backup files (specifically, all `.tar` files) in the
Home Assistant `/backup` directory to a specified path in your Dropbox. This
target path is specified via the `output`option. Once the add-on is started, it
is listening for service calls.

After the add-on is configured and started, trigger an upload by calling the
`hassio.addon_stdin` service with the following service data:

```yaml
service: hassio.addon_stdin
data:
  addon: 782428ea_dropbox-backup
  input:
    command: upload

```

This triggers the `dropbox_uploader.sh` script with the provided access token.
You can use Home Assistant automations or scripts to run uploads at certain
time intervals, under certain conditions, etc.

A sample automation can be found [here](DOCS/sample_automation.md). To use it
simply create a new automation and copy the YAML.

## 📝 License

This add-on is covered under the MIT license refer to [LICENSE.md](LICENSE.md)
for details.
