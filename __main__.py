#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of files2pdf, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#

from __future__ import print_function
import os
import sys
import shutil
import argparse
import unicodedata
import time
import subprocess

home = os.path.expanduser("~")
parser = argparse.ArgumentParser()
parser.add_argument('path',
                    help='path to DIR with files')
parser.add_argument('ext', nargs='?', default='doc',
                    help='what type of files convert to pdf (default: doc)')
args = parser.parse_args()

ext = '.' + args.ext.lower()


def rename(fname):
    def strip_accents(text):
        return ''.join(c for c in unicodedata.normalize(
            'NFKD', text
        ) if unicodedata.category(c) != 'Mn')

    fname = strip_accents(fname.decode(sys.getfilesystemencoding()))
    fname = fname.lower()
    fname = fname.replace(u'\u2013', '-').replace('/', '-')\
        .replace(':', '-').replace(u'\u0142', 'l').replace(' ', '-')\
        .replace('_', '-')
    fname = "".join(x for x in fname if (
        x.isalnum() or x in ('-')
    ))
    return fname.encode(sys.getfilesystemencoding())


for root, dirs, files in os.walk(args.path):
    for f in files:
        if f.lower().endswith(time.strftime("-%d-%m-%Y") + ext):
            continue
        if f.lower().endswith(ext):
            new_name = rename(os.path.splitext(f)[0]) +\
                time.strftime("-%d-%m-%Y") +\
                os.path.splitext(f)[1]
            shutil.copyfile(
                os.path.join(root, f),
                os.path.join(
                    root,
                    new_name
                    )
            )
            os.remove(os.path.join(root, f))
    os.system(
        '/Applications/LibreOffice.app/Contents/MacOS/soffice ' +
        '--headless --convert-to pdf ' +
        args.path + '/*' + ext + ' '
        '--outdir ' + args.path
    )
