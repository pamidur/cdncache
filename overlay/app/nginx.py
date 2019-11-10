import os
import sys
import cdn_lists
from common import *

_service_name = "nginx"

_resolver_conf = "/etc/nginx/resolver.conf"
_map_conf = "/etc/nginx/cachemap.conf"


def _configure_resolver(resolveconf):
    resolver = open(resolveconf, "w")
    addr = getLoopbackAddress()
    if isIp4Address(addr):
        resolver.write("resolver %s;\n" % addr)
    else:
        resolver.write("resolver [%s];\n" % addr)

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

    if os.system("mkdir -p /data/cache/cdncache && chmod -R 666 /data/cache/cdncache && chown -R nobody:nobody /data/cache/cdncache") != 0:
        sys.exit("Cannot create cache folder for nginx")

    _configure_resolver(_resolver_conf)
    _configure_map(_map_conf)

    startService(_service_name)
    print("Nginx Cache Proxy is Ready")


if __name__ == '__main__':
    setup()
