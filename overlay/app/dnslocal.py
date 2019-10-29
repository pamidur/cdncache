import os
import sys
from common import *

service_name = "dnslocal"

service_conf = "/etc/dnsmasq_local.conf"
resolv_conf = "/etc/resolv.conf"

service_conf_template = "/app/templates/dnsmasq_local.template"
resolv_conf_template = "/app/templates/resolv.template"


def configure_resolv(resolveconf):
    writeTemplated(resolv_conf_template, resolveconf,
                   dict(nameserver=getLoopbackAddress()))


def configure_dnslocal(upstreams, dnslocalconf):

    if (len(upstreams) == 0):
        sys.exit("Upstream DNS are not defined")

    servers = ""
    for upstream in upstreams:
        if (ip4_enabled and isIp4Address(upstream)):
            servers += "server=%s\n" % upstream
        if (ip6_enabled and isIp6Address(upstream)):
            servers += "server=%s\n" % upstream

    if (servers == ""):
        sys.exit("Upstream DNS are not supported by current ip configuration")

    writeTemplated(service_conf_template, dnslocalconf, dict(servers=servers))


def setup():
    os.system('supervisorctl stop %s' % service_name)

    configure_dnslocal(upstream_dns, service_conf)
    configure_resolv(resolv_conf)

    os.system('supervisorctl start %s' % service_name)


if __name__ == '__main__':
    setup()