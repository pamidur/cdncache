import os
import sys
import utils

ipv6_enabled = utils.isIpv6Enabled()
ipv4_enabled = utils.isIpv4Enabled()

upstream_dns = os.environ.get('UPSTREAM_DNS').split()

def configure_resolv(resolveconf):
    f = open(resolveconf, "w")
    if(ipv4_enabled):
        f.write("nameserver 127.0.0.1\n")
    if(ipv6_enabled):
        f.write("nameserver ::1\n")
    f.close()

def configure_dnslocal(upstreams, dnslocalconf):
    f = open(dnslocalconf, "w")
    f.writelines(
        ["interface=lo\n"
        , "user=root\n"
        , "no-resolv\n"])

    for upstream in upstreams:
        if(ipv4_enabled and utils.isIpv4Address(upstream)):
            f.write("server=%s\n" % upstream)
        if(ipv6_enabled and utils.isIpv6Address(upstream)):
            f.write("server=%s\n" % upstream)    
    f.close()

os.system('supervisorctl stop dnslocal')

configure_dnslocal(upstream_dns, '/etc/dnsmasq_local.conf')
configure_resolv('/etc/resolv.conf')

os.system('supervisorctl start dnslocal')
