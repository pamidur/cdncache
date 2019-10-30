import dnslocal
import cdn_lists
import cache
import dnsmasq
import sniproxy
from common import *

print("CDN Cache Init")

if len(internal_ips) != 0:
    print("Registering additional ips if needed")

    existingips = getIp4Address("eth0") + getIp6Address("eth0")

    for ip in internal_ips:
        is_plain = ip.split("/")[0]
        if not is_plain in existingips:
            if os.system("ip a a %s dev eth0" % ip) != 0:
                sys.exit("Cannot register internal addresses. Make sure you use --cap-add=NET_ADMIN . Note: INTERNAL_IPS only useful for MACVLAN networks")

dnslocal.setup()
cdn_lists.update()
cache.setup()
sniproxy.setup()
dnsmasq.setup()

print("CDN Cache is Ready")