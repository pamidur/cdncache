import sys
import os
from common import *

sources_dir = "/data/sources/"

__hostnames = None


def __filefilter(x): return x.endswith('.txt')


def __getListOfFiles(dirName, filter):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + __getListOfFiles(fullPath, filter)
        else:
            if(filter(fullPath)):
                allFiles.append(fullPath)

    return allFiles


def getHostnames():
    global __hostnames
    if __hostnames is None:
        __hostnames = dict()
        sourcesfiles = __getListOfFiles(sources_dir, __filefilter)
        for sourcefilepath in sourcesfiles:
            sourcefile = open(sourcefilepath)
            names = filter(lambda x: not x.startswith("#"), map(
                lambda x: x.strip(), sourcefile.readlines()))
            group = os.path.splitext(os.path.basename(sourcefilepath))[0]
            __hostnames[group] = names
            print("Read %s hostnames is group '%s'" % (len(names), group))
            sourcefile.close()
    return __hostnames


def update():

    __hostnames = None

    if(len(params.git_sources) == 0):
        print("No external sources defined. Using what is in '%s'" % sources_dir)
        getHostnames()
        return

    print("Updating CDNs hostnames sources")

    if(os.system("rm -rf %s*" % sources_dir) != 0):
        sys.exit("Cannot cleanup sources dir")

    with cd(sources_dir):
        for source in params.git_sources:
            print("Updating from %s" % source)
            if (os.system("git clone --depth 1 %s" % source) != 0):
                sys.exit("Failed getting sources from %s" % source)
    getHostnames()
    print("CDNs hostnames sources are Updated")


if __name__ == '__main__':
    update()
