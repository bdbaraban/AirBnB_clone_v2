#!/usr/bin/python3
# Fabfile to generates a .tgz archive from the contents of web_static.
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    archive = "web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                   dt.month,
                                                   dt.day,
                                                   dt.hour,
                                                   dt.minute,
                                                   dt.second)
    local("mkdir -p versions")
    local("tar -cvzf versions/{} web_static".format(archive))
