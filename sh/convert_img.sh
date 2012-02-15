#!/bin/sh

CONVERT=convert
DIR=$1
RESIZE_PRC=30%

for i in $DIR/*;
do
    case $i in
        *.JPG|*.jpg|*.jpeg)
            echo "Resizing $i to $RESIZE_PRC"
            $CONVERT -resize $RESIZE_PRC $i $i
        ;;
    *)
        echo "not match"
        ;;
    esac
done
