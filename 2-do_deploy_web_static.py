#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import subprocess

def execute_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_and_deploy_version():
    archive_path = do_pack()
    if archive_path is None:
        return False
    
    # Deploy the version
    if not execute_command(f"sudo mkdir -p /data/web_static/releases/{archive_path}"):
        return False
    if not execute_command(f"sudo tar -xzf {archive_path} -C /data/web_static/releases/{archive_path}"):
        return False
    if not execute_command(f"sudo rm {archive_path}"):
        return False

    # Update the symbolic link
    if not execute_command(f"sudo ln -sf /data/web_static/releases/{archive_path} /data/web_static/current"):
        return False

    # Expose the index.html file
    if not execute_command("sudo cp /data/web_static/current/0-index.html /var/www/html"):
        return False

    return True

# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ['54.146.67.252', '54.90.47.165']


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
