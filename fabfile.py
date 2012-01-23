from time import sleep
from fabric.api import *
from fabric.decorators import runs_once
from fabric.contrib.files import exists
from fabric import utils

import datetime

tarball_filename = 'ucall.zip'
tmp_dir = '/tmp/'
web_dir = '/opt/ucall/'
master_tarball = tmp_dir + tarball_filename
work_tarball = web_dir + tarball_filename

def deploy():
    if not exists(web_dir):
	sudo('mkdir ' + web_dir)

    sudo('rm -rf ' + web_dir + '*')
    sudo('cp ' + master_tarball + ' ' + work_tarball)
    sudo('cd ' + web_dir + ' && unzip ' + work_tarball)
    sudo('rm -f ' + work_tarball)
    sudo('mv ' + web_dir + 'etc/supervisord.conf /etc/supervisor/conf.d/ucall.conf')
    #sudo('pip install -r ' + web_dir + 'requirements1.txt --upgrade')
    #sudo('pip install -r ' + web_dir + 'requirements2.txt --upgrade')

    sleep(1)
    sudo('/etc/init.d/supervisor start')
    sleep(1)

def build(target_environment='staging'):
    local('ant all')
    
def upload_tarball():
    put(master_tarball, tmp_dir)

def all(tagret_environment='staging'):
    build(tagret_environment)
    upload_tarball()
    deploy()