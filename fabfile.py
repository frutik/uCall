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

def _deploy(cmd):
    if not exists(web_dir):
	cmd('mkdir ' + web_dir)

    cmd('rm -rf ' + web_dir + '*')
    cmd('cp ' + master_tarball + ' ' + work_tarball)
    cmd('cd ' + web_dir + ' && unzip ' + work_tarball)
    cmd('rm -f ' + work_tarball)
    cmd('mv ' + web_dir + 'etc/supervisord.conf /etc/supervisor/conf.d/ucall.conf')
    cmd('cd ' + web_dir + 'web/ucall_backend && python manage.py collectstatic')

def deploy():
    if not exists(web_dir):
	sudo('mkdir ' + web_dir)

    sudo('rm -rf ' + web_dir + '*')
    sudo('cp ' + master_tarball + ' ' + work_tarball)
    sudo('cd ' + web_dir + ' && unzip ' + work_tarball)
    sudo('rm -f ' + work_tarball)
    sudo('mv ' + web_dir + 'etc/supervisord.conf /etc/supervisor/conf.d/ucall.conf')

def local_deploy():
    _deploy(local)

def update_requirements():
    sudo('pip install -r ' + web_dir + 'requirements1.txt --upgrade')

def update_src_requirements():
    sudo('cd ' + web_dir + ' && pip install -r ' + web_dir + 'requirements2.txt --upgrade')
    sudo('cd ' + web_dir + 'web/ucall_backend/ && python manage.py collectstatic')

def restore_configs():
    sudo('cp /opt/etc/config,ini ' + web_dir + 'etc/')

def build_source():
    sudo('rm -rf /tmp/ucall/')
    local('ant prepare_3rd_parties copy_source fill_properties')

def build_tarball():
    local('ant prepare_archive')
    
def upload_tarball():
    put(master_tarball, tmp_dir)

def all():
    build_source()
    build_tarball()
    upload_tarball()
    deploy()
    update_requirements()
    
def local_all():
    build_source()
    update_src_requirements()
    
    