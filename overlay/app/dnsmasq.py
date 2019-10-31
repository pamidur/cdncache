import os
import sys
import cdn_lists
from common import *

_service_name = "dnsmasq"

_hosts_dir = "/etc/dnsmasq.d/"
_service_conf = "/etc/dnsmasq.conf"
_service_conf_template = "/app/templates/dnsmasq.template"

def __filterIpList(ip):
    if ip4_enabled and isIp4Address(ip): return True
    if ip6_enabled and isIp6Address(ip): return True
    return False

def _configure_hostfiles(hostsdir):
    if(os.system("rm -rf %s*" % hostsdir)!=0): sys.exit("Cannot cleanup hostfiles dir")

    hostmap = cdn_lists.getHostnames()
    ips = filter(__filterIpList, external_ips)
    ipsstr = ""
    for ip in ips: ipsstr += ",%s" % ip

    hostfiles = []

    for group in hostmap.keys(): 
        names = hostmap[group]
        if len(names) != 0:
            
            hostfilepath = os.path.join(_hosts_dir,group + ".hosts")
            hostfile = open(hostfilepath, "w")  
            host="%s.cdncache" % group

            hostfile.write("auth-zone=%s\n" % host)
            hostfile.write("host-record=%s%s\n" % (host, ipsstr))             

            for name in names:
                if name.startswith("*."):
                    hostfile.write("auth-zone=%s\n" % name[2:])                  
                    hostfile.write("cname=%s,%s\n" % (name,host))
                else:
                    hostfile.write("host-record=%s%s\n" % (name, ipsstr))  
                
            hostfile.close
            hostfiles.append(hostfilepath)
            print("Written hosts file for '%s'" % group)
    
    return hostfiles

def _configure_dnsmasq(forwarddns, hostsfiles, serviceconf):

    servers = ""
    for upstream in forwarddns:
        if (ip4_enabled and isIp4Address(upstream)):
            servers += "server=%s\n" % upstream
        if (ip6_enabled and isIp6Address(upstream)):
            servers += "server=%s\n" % upstream

    writeTemplated(_service_conf_template, serviceconf, dict(servers=servers))


def setup():
    print("Configuring external DNS")
    stopService(_service_name)

    hostsfiles = _configure_hostfiles(_hosts_dir)
    _configure_dnsmasq(forward_dns, hostsfiles, _service_conf)

    startService(_service_name)
    print("Exterenal DNS is Ready")

if __name__ == '__main__':
    setup()