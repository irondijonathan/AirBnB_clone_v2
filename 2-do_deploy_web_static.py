#!/usr/bin/python3
"""
 Fabric script that distributes
 an archive to your web servers, using the function do_deploy
"""
import os
from datetime import datetime
from fabric.api import put, runs_once, env, run, local

env.user = 'ubuntu'
env.hosts = ['100.26.9.42', '54.237.115.35']


@runs_once
def do_pack():
    """Archives the static files."""
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


def do_deploy(archive_path):
    """Uploads and unpacks an archive on the server"""

    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    output_dir = archive_name.split('.')[0]
    r_dir = "/data/web_static/releases/"
    res = False
    try:
        put(archive_path, "/tmp")
        run(f"mkdir -p {r_dir}{output_dir}")
        run(f"tar -xzf /tmp/{archive_name} -C {r_dir}{output_dir}/")
        run(f"rm /tmp/{archive_name}")
        run(f" mv {r_dir}{output_dir}/web_static/* {r_dir}{output_dir}/")
        run(f"rm -rf {r_dir}{output_dir}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {r_dir}{output_dir}/ /data/web_static/current")
        print('New version deployed!')
        res = True
    except Exception:
        res = False

    return res
