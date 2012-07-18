#!/bin/sh

import sys, os, re

hfs_dir = ""
if len(sys.argv) != 3:
    print sys.argv[0], '<hfs2_source_code_dir>', '<hfs2_server_url>'
    exit()

hfs_dir = sys.argv[1]
hfs_url = sys.argv[2]
if '://' not in hfs_url:
    hfs_url = 'http://' + hfs_url

suffixes = ('tpl', 'pas')

groups = []

files = os.listdir(hfs_dir)
for filename in files:
    ignore = True
    for suffix in suffixes:
        if filename.endswith(suffix):
            ignore = False
            break

    if ignore:
        continue

    with open(os.path.join(hfs_dir, filename)) as f:
        for line in f:
            m = re.findall('href\s*=\s*"([^"]*)"', line)
            if len(m) != 0:
                groups.extend(m)

            m = re.findall('src\s*=\s*"([^"]*)"', line)
            if len(m) != 0:
                groups.extend(m)

            continue

items = []

for item in groups:
    if item[:1] == '/':
        item = item[1:]

    if item[:1] != '~':
        continue

    pos = item.find(' ')
    if pos != -1:
        continue

    pos = item.find('?')
    if pos != -1:
        item = item[:pos]

    if item == '':
        continue

    if item in items:
        continue

    if item[:4] != '~img':
        continue

    items.append(item)

for item in items:
    item_url = hfs_url + '/' + item
    os.system('curl ' + item_url + ' > ' + item[1:] + '.gif')


os.system('curl ' + hfs_url + '/favicon.ico > favicon.ico')
