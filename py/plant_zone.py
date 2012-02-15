#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os, sys

import Image

cwd = os.path.abspath(os.path.dirname(__file__))
image_dir = os.path.join(cwd, '../plant_zone')
thumbnails_dir = os.path.join(image_dir, 'thumbnails')
index_html = 'index.html'

html_template = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <title>%(title)s</title>
    <link rel="stylesheet" type="text/css" href="/css/bootstrap.css" />
    <link rel="stylesheet" type="text/css" href="/css/lightbox.css" media="screen" />

    <script type="text/javascript" src="/js/gallery.js"></script>
    <script type="text/javascript" src="/js/prototype.js"></script>
    <script type="text/javascript" src="/js/scriptaculous.js?load=effects,builder"></script>
    <script type="text/javascript" src="/js/lightbox.js"></script>

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  </head>
  <body>
  <div class="alert-message blcok-message">
    <p>
    <a class="btn large primary" href="plant_zone/plant_zone.tgz">亲，点我下载高清无码图回去慢慢看吧</a>
    </p>
  </div>
    <div id="wrapper">
      %(body_content)s
    </div>

  </body>
</html>'''

def mkdir(path):
    if not os.path.exists(path):
        print 'mkdir', path
        os.makedirs(path)

def generate_html(keys):
    return html_template % keys

def make_links(imgfile, is_main=False):
    bf = os.path.basename(imgfile)
    fn, ext = os.path.splitext(bf)
    thumb_fn = fn + '_thumb' + ext
    img_parent_dir = os.path.split(image_dir)[-1]
    img_link_src = os.path.join(img_parent_dir, bf)
    thumb_link_src = os.path.join(img_parent_dir, 'thumbnails', thumb_fn)
    # chunk = ['<a rel="lightbox[plant]"><img  src="%(img_link_src)s" id="imgPhoto" alt="%(bf)s" height="500" width="375" /><p id="caption">%(bf)s</p></a>']
    chunk = ('<a href="%(img_link_src)s" rel="lightbox[plant]">'
            '<img src="%(thumb_link_src)s" class="thumbnail" /></a>\n')

    # chunk.append('''<a href="%(img_link_src)s" onclick="javascript:swapPhoto('%(img_link_src)s', '%(bf)s'); return false;">
         # <img src="%(thumb_link_src)s" alt="sheep" width="100" height="75" /></a>''')

    return chunk % {'img_link_src': img_link_src, 'thumb_link_src': thumb_link_src}


def make_thumbnail(infile):
    bf = os.path.basename(infile)
    fn, ext = os.path.splitext(bf)
    thumbnail_img = fn + '_thumb' + ext
    outfile = os.path.join(thumbnails_dir, thumbnail_img)
    mkdir(thumbnails_dir)
    if os.path.exists(outfile):
        return
    try:
        im = Image.open(infile)
        im.thumbnail((128, 128))
        im.save(outfile, "JPEG")
    except IOError, e:
        print >> sys.stderr, "Connot convert %s, %s" % (infile, e)
        pass

def is_image(infile):
    img_exts = ['.jpg', '.jpeg', '.gif', '.png']
    bf = os.path.basename(infile)
    fn, ext = os.path.splitext(bf)
    if ext.lower() in img_exts:
        return True
    return False

def main():
    chunk = []
    for f in os.listdir(image_dir):
        if is_image(f):
            make_thumbnail(os.path.join(image_dir, f))
            chunk.append(make_links(f))
    print html_template % {'title': '植物园一日游', 'body_content': ''.join(chunk)}

if __name__ == "__main__":
    main()
