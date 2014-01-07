#! /usr/bin/python

import os
from pprint import pprint

filename = 'yumpkginfo.txt'


def gen_pkgperurl():
    urldict = {}
    prevpkg = ''
    fp = open(filename)
    for l in fp:
        splits = l.split(':')
        tag = splits[0].strip()
        value = ':'.join(splits[1:]).strip()
        if tag == 'Name':
            prevpkg = value 
        elif tag == 'URL':
            #print value, splits[1]
            pkgnames = urldict.setdefault(value, [])
            pkgnames.append(prevpkg)
    fp.close()
    pprint(urldict)

def gen_pkginfo():
    fp = open(filename, 'w')
    for l in os.popen("yum info | grep -E '^Name|^URL'"):
        fp.write(l)
    fp.close()

def main():
    if not os.path.exists(filename):
        gen_pkginfo()
    gen_pkgperurl()


if __name__ == '__main__':
    main()
