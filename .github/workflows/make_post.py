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

    fi = os.path.join(path, 'details.txt')
    body = os.path.join(path, 'contents.txt')
    with codecs.open(fi, 'r', 'utf-8') as f:
        details = json.load(f)
    with codecs.open(body, 'r', 'utf-8') as f:
        contents = f.read()

    date = parser.parse(details['published_date'])
    title = details['release_name']

    filename = os.path.join(path, date.strftime('%Y-%m-%d') + '-' + title.lower().replace(' ', '-') + '.md')
    print(filename)
    md = POST.format(title, details['published_date'], 'Sigil', contents)
    print(md)
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(md)

    '''
    try:
        with open(p, 'w') as f:
            f.write('\n'.join(remote))
            f.write('\n')
    except Exception:
        sys.exit(2)
    print('Updates from remote versions')
    '''
    sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
