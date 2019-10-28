import os

def isIpv4Enabled():
    result = os.popen('ip a | grep -w inet').read()
    return result != ""

def isIpv6Enabled():
    result = os.popen('ip a | grep -w inet6').read()
    return result != ""

def isIpv4Address(address):
    return "." in address;

def isIpv6Address(address):
    return ":" in address;