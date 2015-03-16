#! /usr/bin/python

import os

# Currently cache file is unintelligent
# Todo: Use yum history to smartly determine if
# the cache file is stale or Ok to use
filename = 'yumpkginfo.txt'


def gen_pkgperurl():
    urldict = {}
    prevpkg = ''
    fp = open(filename)
    # Read each line
    for l in fp:
        splits = l.split(':')
        tag = splits[0].strip()
        value = ':'.join(splits[1:]).strip()
        # It has been observed that some info for packages
        # do not have corresponding URL. Such cases
        # are automatically handled by ignoring such packages
        # in our analysis
        if tag == 'Name':
            prevpkg = value 
        elif tag == 'URL':
            # Use set instead of list to avoid duplicate entries of
            # packages with same name but diffrent architectures
            pkgnameset = urldict.setdefault(value, set())
            pkgnameset.add(prevpkg)
    fp.close()
    return urldict

def gen_pkginfo():
    fp = open(filename, 'w')
    for l in os.popen("yum info | grep -E '^Name|^URL'"):
        fp.write(l)
    fp.close()

def print_urldict(urldict):
    for (url, pkgset) in urldict.items():
        print url
        for pkg in pkgset:
            print pkg
        print

def main():
    # First check if cache file exists
    if not os.path.exists(filename):
        # Generate cache file if does not exist
        gen_pkginfo()

    # Now run the analysis
    urldict = gen_pkgperurl()
    print_urldict(urldict)


if __name__ == '__main__':
    main()
