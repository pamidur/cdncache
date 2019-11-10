import os
import sys
import cdn_lists
from common import *

_service_name = "nginx"

_resolver_conf = "/etc/nginx/resolver.conf"
_map_conf = "/etc/nginx/cachemap.conf"


def _configure_resolver(resolveconf):
    resolver = open(resolveconf, "w")
    resolver.write("resolver %s;\n" % getLoopbackAddress())
    resolver.close()


def _configure_map(mapconf):

    hostmap = cdn_lists.getHostnames()

    mapfile = open(mapconf, "w")

    for group in hostmap.keys():
        for name in hostmap[group]:
            mapfile.write("%s\t%s;\n" % (name, group))

    mapfile.close()


def setup():
    print("Configuring Nginx Cache Proxy")
    stopService(_service_name)

    _configure_resolver(_resolver_conf)
    _configure_map(_map_conf)

    startService(_service_name)
    print("Nginx Cache Proxy is Ready")


if __name__ == '__main__':
    setup()
