#!/usr/bin/env python

import sys
import os

PRJ_DIR='/data/htdocs/todo'

CONTROLLER_TPL='''
<?php
/**
* Tasks
*/
class Controller_%s extends Controller_Abstract
{
    function actionIndex()
    {
    }
}

?>
'''

def mkdir(path):
    if not os.path.exists(path):
        print 'mkdir %s' % path
        os.makedirs(path)

def writefile(filepath, content):
    print 'Create file %s' % filepath
    with open(filepath, 'wb') as fb:
        fb.write(content)

def create_controller(cname):
    cv_dir = os.path.join(PRJ_DIR, 'app/view', cname.lower())
    c_file = os.path.join(PRJ_DIR, 'app/controller', '%s_controller.php' % cname.lower())
    mkdir(cv_dir)
    writefile(c_file, CONTROLLER_TPL % cname.capitalize())

if __name__ == "__main__":
    create_controller(sys.argv[1])


