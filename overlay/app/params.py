import os
import sys

internal_ips = os.environ.get('INTERNAL_IPS')
if internal_ips is None or internal_ips == "":
    internal_ips = []
else:
    internal_ips = internal_ips.split()

external_ips = os.environ.get('EXTERNAL_IPS')
if external_ips is None or external_ips == "":
    external_ips = map(lambda x: x.split("/")[0], internal_ips)
else:
    external_ips = external_ips.split()

if len(external_ips) == 0:
    sys.exit("No IPs defined. Define at least one external or internal ip.")

upstream_dns = os.environ.get('UPSTREAM_DNS')
if upstream_dns is None or upstream_dns == "":
    sys.exit("'UPSTREAM_DNS' is not defined")
upstream_dns = upstream_dns.split()

forward_dns = os.environ.get('FORWARD_DNS')
if (forward_dns is None):
    forward_dns = upstream_dns
else:
    forward_dns = forward_dns.split()

git_sources = os.environ.get('GIT_SOURCES', "")
git_sources = git_sources.split()

prefer_ip6 = bool(os.environ.get('PREFER_IP6', 'True'))
