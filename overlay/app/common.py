import os
from params import *
from string import Template


def checkIp4Enabled():
    result = os.popen('ip a | grep -w inet').read()
    return result != ""


def checkIp6Enabled():
    result = os.popen('ip a | grep -w inet6').read()
    return result != ""


def isIp4Address(address):
    return "." in address


def isIp6Address(address):
    return ":" in address


def getIp4Address(interface):
    return getIpAddress(interface, "inet")


def getIp6Address(interface):
    return getIpAddress(interface, "inet6")


def getIpAddress(interface, atype):
    chunks = os.popen("ip addr show %s" % interface).read().split("%s " %
                                                                  atype)
    if (len(chunks) == 1):
        return []
    return map(lambda x: x.split("/")[0], chunks[1:])


def getLoopbackAddress():
    if (prefer_ip6):
        addrs = getIp6Address("lo")
        if (len(addrs) == 0):
            addrs = getIp4Address("lo")
    else:
        addrs = getIp4Address("lo")
        if (len(addrs) == 0):
            addrs = getIp6Address("lo")

    if (len(addrs) == 0):
        sys.exit("Cannot figure out loopback address")

    return addrs[0]


def writeTemplated(template_path, target_path, values):
    template = open(template_path)
    data = Template(template.read())
    template.close()
    data = data.substitute(values)

    target = open(target_path, "w")
    target.write(data)
    target.close()


class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def stopService(service):
    if (os.popen('supervisorctl pid %s' % service).read().rstrip() != "0"):
        if (os.system('supervisorctl stop %s' % service) != 0):
            sys.exit("Cannot stop service '%s'" % service)


def startService(service):
    if (os.popen('supervisorctl pid %s' % service).read().rstrip() == "0"):
        if (os.system('supervisorctl start %s' % service) != 0):
            sys.exit("Cannot start service '%s'" % service)


ip4_enabled = checkIp4Enabled()
ip6_enabled = checkIp6Enabled()

if (not ip4_enabled and not ip6_enabled):
    sys.exit("Ip protocol misconfiguration.")