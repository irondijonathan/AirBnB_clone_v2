#!/usr/bin/python3
"""
This is a Fabric script that generates a .tgz archive
from the contents of the web_static folder of
the AirBnB Clone repo, using the function do_pack
"""
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """This Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    filename = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(filename))
        local("tar -cvzf {} web_static".format(filename))
        archize_size = os.stat(filename).st_size
        print(
            "web_static packed: {} -> {} Bytes".format(filename, archize_size))
    except Exception:
        filename = None
    return filename
