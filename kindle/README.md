scp the script to `/mnt/us/`

Enable rw on root

```
mntroot rw
```

add the script to `/etc/crontab/root`

```
0 6 * * * /mnt/us/fetch.sh
```

You might have to kill cron on your kindle (or reboot) to apply these changes
