#!/bin/sh

APP_SH=$(dirname $0)
. $APP_SH/rsync_env.sh


chmod 600 $APP/rsync/conf/rsyncd.passwd
chmod 600 $APP/rsync/conf/rsyncd.conf

$APP/rsync/bin/rsync --daemon --config=$APP/rsync/conf/rsyncd.conf  --port=8730 &





