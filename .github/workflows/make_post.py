import os
import sys
import getopt
import json
import codecs
from dateutil import parser


BAIL = False

NAME = 'Sigil'

POST = """---
title: {}
date: {}
categories:
  - Blog
tags:
  - Releases
  - {}
---

{{% include remote_versions.html %}}
{}

Latest Sigil Version {{{{ sigil_ver }}}}
"""

asset_patterns = {
    'CHECKSUMS.sha256.txt'  : 'CHECKSUMS file',
    'Windows-Setup.exe'     : 'Windows x86 download',
    'Windows-x64-Setup.exe' : 'Windows x64 download',
    'Mac.txz'               : 'MacOS download'
}

link = "[{}]({}){{: .btn .btn--success}}<br/>"

def get_asset_urls(assets, tag):
    md_links =[]
    for asset in assets:
        for p, t in asset_patterns.items():
            if p in asset['name']:
                md_links.append(link.format(t, asset['browser_download_url']))

    print(md_links)


def main(argv):
    global BAIL
    global POST
    path = ''
    try:
        opts, args = getopt.getopt(argv,"hp:",["path="])
    except getopt.GetoptError:
        print ('make_post.py -p <path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('make_post.py -p <path>')
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg

    with codecs.open(path, 'r', 'utf-8') as f:
        j = json.load(f)
    r = j['release']
    tag = r['tag_name']
    date = parser.parse(r['published_at'])
    title = r['name']

    filename = os.path.join('.', date.strftime('%Y-%m-%d') + '-' + title.lower().replace(' ', '-') + '.md')
    print(filename)
    get_asset_urls(r['assets'], tag)
    md = POST.format(title, r['published_at'], NAME, r['body'])
    print(md)
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(md)

    sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
