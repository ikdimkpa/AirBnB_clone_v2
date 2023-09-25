#!/usr/bin/python3

"""a Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack.
"""

import os.path

from fabric.api import local
from datetime import datetime
from fabric.api import env
from fabric.api import put
from fabric.api import run


env.hosts = ["54.174.230.152", "54.160.103.251"]


def do_pack():
    """a function that generates a .tgz archive from the contents of the
    web_static folder.
    """
    if not (os.path.isdir('versions')):
        local('mkdir versions')

    d = datetime.now()
    date = f"{d.year}{d.month}{d.day}{d.hour}{d.minute}{d.second}"
    path = f"versions/web_static_{date}.tgz"

    result = local(f"tar -cvzf {path} web_static")

    if result.failed:
        return None
    return path


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns (bool):
        Returns False if the file doesn't exist at archive_path or an error
        occurs, Otherwise, return True.
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


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
