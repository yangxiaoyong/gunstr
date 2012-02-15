#!/bin/sh

# 将数据库直接导入到另一台机器上
mysqldump --add-drop-table --extended-insert --force --log-error=error.log -uUSER -pPASS OLD_DB_NAME | ssh -C user@newhost "mysql -uUSER -pPASS NEW_DB_NAME"

# 就是个浪费带宽的事，蛋疼的玩意
dd if=/dev/zero bs=1M | ssh somesite dd of=/dev/null

# 打印二行数字之间的内容
sed -n '3,6p' /path/to/file

# 打印二行数字之间的内容
awk 'NR >= 3 && NR <= 6' /path/to/file

# Get rid of multiple spaces/tabs in a text file
# This command does the following:
# - converts any sequence of multiple spaces/tabs to one space only
# - completely removes any space(s)/tab(s) at the end of each line
sed -i "s/\(\x09\{1,\}\)\|\( \{1,\}\)/ /g;s/\(\x09\{1,\}$\)\|\( \{1,\}$\)//g" brisati.txt

