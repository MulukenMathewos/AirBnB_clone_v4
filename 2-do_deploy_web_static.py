#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['54.146.67.252', '54.90.47.165']


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the folder /data/web_static/releases/<archive filename without extension>
        file_name = archive_path.split('/')[-1]
        folder_name = '/data/web_static/releases/' + file_name.split('.')[0]
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, folder_name))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}/web_static/* {}'.format(folder_name, folder_name))
        run('rm -rf {}/web_static'.format(folder_name))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current linked to the new version
        run('ln -s {} /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print(str(e))
        return False
