# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
import os
from fabric.api import env, local, run
from fabric.contrib.files import append, exists, sed

REPO = 'https://github.com/MakingThingsHappen/thumborweb.git'


def deploy():
    site_folder = os.path.join('/home', str(env.user), 'sites', str(env.host))
    source_folder = os.path.join(site_folder, 'src')
    _get_latest_source(site_folder)
    _create_directory_structure_if_necessary(site_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(site_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _get_latest_source(site_folder):
    if exists(os.path.join(site_folder, '.git')):  #
        run('cd %s && git fetch' % (site_folder,))  #
    else:
        run('git clone %s %s' % (REPO, site_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)  #
    run('cd %s && git reset --hard %s' % (site_folder, current_commit))


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('static', 'virtualenv'):
        run('mkdir -p {}'.format(os.path.join(site_folder, subfolder)))


def _update_settings(source_folder, site_name):
    settings_path = os.path.join(source_folder, 'thumborweb', 'settings', 'production.py')
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)  #
        )
    secret_key_file = os.path.join(source_folder, 'thumborweb', 'settings', 'secret_key.py')
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(site_folder):
    virtualenv_folder = os.path.join(site_folder, 'virtualenv')
    if not exists(virtualenv_folder + '/bin/pip'):  #
        run('virtualenv --python=python %s' % (virtualenv_folder,))
    run('{}/bin/pip install -r {}'.format(
        virtualenv_folder,
        os.path.join(site_folder, 'requirements', 'production.txt')))


def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python manage.py collectstatic --noinput' % (  #
        source_folder,
    ))


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python '
        'manage.py makemigrations --noinput'.format(source_folder))
    run('cd %s && ../virtualenv/bin/python '
        'manage.py migrate --noinput'.format(source_folder))
