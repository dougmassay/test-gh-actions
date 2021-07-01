import os
import sys
import getopt
import json
import codecs
from dateutil import parser


BAIL = False

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
    date = parser.parse(r['published_at'])
    title = r['name']

    filename = os.path.join('.', date.strftime('%Y-%m-%d') + '-' + title.lower().replace(' ', '-') + '.md')
    print(filename)
    md = POST.format(title, r['published_at'], 'Sigil', r['body'])
    print(md)
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(md)

    sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
