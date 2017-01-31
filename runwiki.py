# -*- coding: utf-8 -*-

import os
from glob import glob
from flask import Flask, abort, redirect
from markdown import markdown

app = Flask(__name__)

def load_files():
    files = [filename for filename in glob('*.md')]
    anchors = ['[%s]: /%s' % (filename.strip('.md'), filename.strip('.md')) for filename in files]
    return '\n'.join(anchors)

@app.route('/')
def index():
    return redirect('/Home')

@app.route("/<filename>")
def show_wiki(filename):
    filename_ext = '%s.md' % filename
    if not os.path.exists(filename_ext):
        abort(404)
    title = filename
    with open(filename_ext) as f:
        body = f.read()
        body += '\n'
        body += load_files()
        body = markdown(body)
    return '<html><head><title>%(title)s</title></head><body>%(body)s</body></html>' % dict(
        title=title,
        body=body,
    )

if __name__ == '__main__':
    app.run(debug=True)
