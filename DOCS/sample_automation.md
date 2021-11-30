# Sample automation

```yaml
alias: Automatic backup and upload
description: Makes a backup and uploads it to Dropbox at 1:00.
mode: single

# Trigger each day at 1:00
trigger:
  - platform: time
    at: '1:00'

condition: []

action:

  # Make a backup
  - service: hassio.backup_full
    data_template:
      name: Automated Backup {{ now().strftime('%Y-%m-%d') }}

  # Upload to Dropbox
  - service: hassio.addon_stdin
    data:
      addon: 782428ea_dropbox-backup
      input:
        command: upload

```
