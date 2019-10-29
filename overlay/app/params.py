import os
import sys

upstream_dns = os.environ.get('UPSTREAM_DNS')
if (upstream_dns is None):
    sys.exit("'UPSTREAM_DNS' is not defined")
upstream_dns = upstream_dns.split()

git_sources = os.environ.get('GIT_SOURCES')
if (git_sources is None):
    sys.exit("'GIT_SOURCES' is not defined")
git_sources = git_sources.split()

prefer_ip6 = os.environ.get('PREFER_IP6', True)