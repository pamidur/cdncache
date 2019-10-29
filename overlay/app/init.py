import dnslocal
import cdn_lists
import cache
import dnsext
import sniproxy

dnslocal.setup()
cdn_lists.update()
cache.setup()
sniproxy.setup()
dnsext.setup()
