# -*- coding: utf-8 -*-

import re
import os
from glob import glob
from flask import Flask, abort, redirect
from markdown import markdown

app = Flask(__name__)

def load_files():
    files = [filename for filename in glob('*.md')]
    files.extend(filename for filename in glob('*/*.md'))
    files.extend(filename for filename in glob('*/*/*.md'))
    files = map(lambda filename: filename.decode('utf8'), files)
    files = map(lambda filename: re.sub(r'(.*).md', r'\1', filename), files)
    files = map(lambda filename: u'[%s]: /%s' % (filename, filename), files)
    return u'\n'.join(files)

@app.route('/')
def index():
    return redirect('/Home')

@app.route("/<path:filename>")
def show_wiki(filename):
    filename_ext = '%s.md' % filename
    if not os.path.exists(filename_ext):
        abort(404)
    title = filename
    with open(filename_ext) as f:
        body = f.read()
        body += '\n'
        body = body.decode('utf8')
        body += load_files()
        body = markdown(body)
    return '<html><head><title>%(title)s</title></head><body>%(body)s</body></html>' % dict(
        title=title,
        body=body,
    )

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        app.run(debug=False, port=sys.argv[1])
    else:
        app.run(debug=True)
