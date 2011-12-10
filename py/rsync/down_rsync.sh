#!/bin/sh

APP_SH=$(dirname $0)
. $APP_SH/rsync_env.sh


ip=$1
APPOBJ=$2
del=$3


RSYNC_PASSWORD=$APP/rsync/conf/rsync.password

chmod 600 $RSYNC_PASSWORD

$APP/rsync/bin/rsync -avzptL $del --password-file=$RSYNC_PASSWORD rsync://fetip@$ip:8730/apps/$APPOBJ/ $APP/$APPOBJ/


