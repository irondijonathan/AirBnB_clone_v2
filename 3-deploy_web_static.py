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
    """Uploads and unpacks an archive on the server
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    archive_name = os.path.basename(archive_path)
    folder_name = archive_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(archive_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, folder_path))
        run("rm -rf /tmp/{}".format(archive_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
