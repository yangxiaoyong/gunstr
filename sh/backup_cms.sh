#!/bin/sh

tar zcf /apps/bak/228_dat_www_$(date +%F).tgz /apps/dat/www/
/apps/sh/dump_pg.sh
