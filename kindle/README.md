scp the script to `/mnt/us/`

Enable rw on root

```
mntroot rw
```

add the script to `/etc/crontab/root`

```
0 6 * * * /mnt/us/fetch.sh
```

