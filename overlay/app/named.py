import os
import sys
import cdn_lists
from common import *

_service_name = "named"

_hosts_dir = "/etc/bind/"
_service_conf = "/etc/bind/options.conf"
_service_conf_template = "/app/templates/named.template"
_service_zone = "/etc/bind/cdncache.db"
_service_zone_template = "/app/templates/cdncache.template"
_service_rpz = "/etc/bind/rpz.db"
_service_rpz_template = "/app/templates/rpz.template"


def __filterIpList(ip):
    if ip4_enabled and isIp4Address(ip):
        return True
    if ip6_enabled and isIp6Address(ip):
        return True
    return False


def _configure_zones(zone_file, rpz_file, externalips):

    hostmap = cdn_lists.getHostnames()
    ips = filter(__filterIpList, externalips)

    zone_records = ""
    rpz_records = ""

    for group in hostmap.keys():
        names = hostmap[group]
        if len(names) != 0:

            for ip in ips:
                type = "A" if isIp4Address(ip) else "AAAA"
                zone_records += "%s IN %s %s;\n" % (group, type, ip)

            for name in names:
                rpz_records += "%s IN CNAME %s.cdncache.;\n" % (name, group)

            print("Written hosts file for '%s'" % group)

    writeTemplated(_service_zone_template, zone_file,
                   dict(records=zone_records))

    writeTemplated(_service_rpz_template, rpz_file, dict(records=rpz_records))


def _configure_named(forwarddns, serviceconf):

    forwarders = ""
    for upstream in forwarddns:
        if (ip4_enabled and isIp4Address(upstream)):
            forwarders += "%s; " % upstream
        if (ip6_enabled and isIp6Address(upstream)):
            forwarders += "%s; " % upstream

    if ip4_enabled:
        listen4 = ""
        for ip in getIp4Address("eth0"):
            listen4 += "%s; " % ip
    else: listen4 = "none; "

    if ip6_enabled:
        listen6 = ""
        for ip in getIp6Address("eth0"):
            listen6 += "%s; " % ip
    else: listen6 = "none; "

    writeTemplated(_service_conf_template, serviceconf, dict(forward=forwarders, listen4 = listen4, listen6 = listen6))


def setup():
    print("Configuring external DNS")
    stopService(_service_name)

    _configure_zones(_service_zone, _service_rpz, params.external_ips)
    _configure_named(params.forward_dns, _service_conf)

    startService(_service_name)
    print("Exterenal DNS is Ready")


if __name__ == '__main__':
    setup()
