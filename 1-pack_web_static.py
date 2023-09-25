#!/usr/bin/python3

"""a Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack.
"""

import os.path

from fabric.api import local
from datetime import datetime


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
