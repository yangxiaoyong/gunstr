#!/bin/sh
# qee

PRJ_DIR=/data/htdocs/todo
CONTROLLER=$1

EOF <<<
<?php
/**
* Tasks
*/
class Controller_${1} extends Controller_Abstract
{
    function actionIndex()
    {
    }
}

?>
EOF

echo create file $PRJ_DIR/app/controller/${CONTROLLER}_controller.php
touch $PRJ_DIR/app/controller/${CONTROLLER}_controller.php
echo mkdir $PRJ_DIR/app/view/${CONTROLLER}
mkdir -p $PRJ_DIR/app/view/${CONTROLLER}
