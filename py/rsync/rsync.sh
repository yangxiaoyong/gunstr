#!/bin/sh
ip=$1
src_data=$2
des_data=$3
bwlimit=$4

RSYNC_PASSWORD=/apps/rsync/conf/rsync.password

chmod 600 $RSYNC_PASSWORD

/apps/rsync/bin/rsync -avzpt --bwlimit=$bwlimit --password-file=$RSYNC_PASSWORD rsync://fetip@$ip:8730$src_data $des_data


