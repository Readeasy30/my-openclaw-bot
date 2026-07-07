# my-openclaw-bot

Automated Windows 11 maintenance framework powered by GitHub repository polling.

## Command Index (`maintenance_jobs.txt`)
* `CHECK_SERVICES` : Monitor critical Windows services and force a restart if they crash.
* `INSTALL_UPDATES` : Remotely trigger downloads and force-install all pending OS patches (Auto-reboots if required).
* `SYSTEM_ALERTS` : Check real-time CPU, RAM capacity margins, and run Windows Update status audits.
* `LIST_DISPLAYS` : Pull active hardware layout strings.
* `RESET_DISPLAYS` : Force graphical driver refresh.
* `ARRANGE_DISPLAYS` : Force panoramic presentation orientation.
* `DISK_CHECK` : Fetch healthy logical partition arrays.
* `CLEAR_TEMP` : Purge transient workspace allocations.

## Outputs
Review runtime operational telemetry logs inside `maintenance_log.txt`.
