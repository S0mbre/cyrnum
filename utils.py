# -*- coding: utf-8 -*-

import os, base64, tempfile, uuid, traceback, imghdr

def print_traceback(**kwargs):
    traceback.print_exc(**kwargs)

def abspath(file, root=None):
    if not root:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, file)

def guid(no_hyphens=True):
    u = uuid.uuid4().hex
    if no_hyphens: u = u.replace('-', '')
    return u

def tmpfile(root=None, ext=None, basename=False):
    root = root or tempfile.gettempdir()
    fname = guid()
    if ext: fname += f'.{ext}'
    return fname if basename else abspath(fname, root)

def b64img_encode(img, ext=None, enc='utf-8'):
    isfile = isinstance(img, str)
    ext = ext or (imghdr.what(img) if isfile else imghdr.what('', img)) or 'png'
    prefix = f'data:image/{ext};base64,'
    try:
        if isfile:
            with open(img, 'rb') as file_:
                s = base64.b64encode(file_.read())
        else:
            s = base64.b64encode(img)
        return prefix + s.decode(enc)
    except:
        print_traceback()
        return prefix