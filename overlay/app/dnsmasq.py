import os
import sys
from common import *

service_name = "dnsmasq"

service_conf = "/etc/dnsmasq.conf"
resolv_conf = "/etc/resolv.conf"

service_conf_template = "/app/templates/dnsmasq.template"
resolv_conf_template = "/app/templates/resolv.template"


def configure_resolv(resolveconf):
    writeTemplated(resolv_conf_template, resolveconf,
                   dict(nameserver=getLoopbackAddress()))


def configure_dnslocal(upstreams, dnslocalconf):

    if (len(upstreams) == 0):
        sys.exit("Upstream DNS are not defined")

    servers = ""
    for upstream in upstreams:
        ip_plain = upstream.split('#')[0]
        if (ip4_enabled and isIp4Address(ip_plain)):
            servers += "server=%s\n" % upstream
        if (ip6_enabled and isIp6Address(ip_plain)):
            servers += "server=%s\n" % upstream

    if (servers == ""):
        sys.exit("Upstream DNS are not supported by current ip configuration")

    writeTemplated(service_conf_template, dnslocalconf, dict(servers=servers))


def setup():
    print("Configuring local DNS")
    stopService(service_name)

    configure_dnslocal(params.upstream_dns, service_conf)
    configure_resolv(resolv_conf)

    startService(service_name)
    print("Local DNS is Ready")

if __name__ == '__main__':
    setup()