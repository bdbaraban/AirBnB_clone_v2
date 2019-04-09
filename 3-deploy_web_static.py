#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
from fabric.api import env

do_pack = __import__("1-pack_web_static").do_pack
do_deploy = __import__("2-do_deploy_web_static").do_deploy

env.hosts = ["104.196.168.90", "35.196.46.172"]


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
