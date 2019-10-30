import os
import sys
from common import *

service_name = "sniproxy"
service_conf = "/etc/sniproxy.conf"
service_conf_template = "/app/templates/sniproxy.template"

# * ipv4_only   query for IPv4 addresses (default)
# * ipv6_only   query for IPv6 addresses
# * ipv4_first  query for both IPv4 and IPv6, use IPv4 is present
# * ipv6_first  query for both IPv4 and IPv6, use IPv6 is present


def setup():
    print("Configuring sniproxy")
    stopService(service_name)

    mode = None

    if (ip4_enabled and not ip6_enabled): mode = "ipv4_only"
    if (ip6_enabled and not ip4_enabled): mode = "ipv6_only"
    if (ip4_enabled and ip6_enabled and prefer_ip6): mode = "ipv6_first"
    else:
        if (ip4_enabled and ip6_enabled): mode = "ipv4_first"

    writeTemplated(service_conf_template, service_conf,
                   dict(nameserver=getLoopbackAddress(), mode=mode))

    startService(service_name)
    print("Sniproxy is Ready")


if __name__ == '__main__':
    setup()
