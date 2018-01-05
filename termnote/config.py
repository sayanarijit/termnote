# -*-coding: utf-8 -*-
'''
Author:         Arijit Basu
Email:          sayanarijit@gmail.com
Documentation:  https://sayanarijit.github.io/note.py
'''

import os


VERSION = 'v1.0.9'
EDITOR = os.environ.get('EDITOR', 'vi')
STORAGE = os.environ.get('TN_STORAGE', os.path.expanduser('~') + '/.termnote')
SCREEN_WIDTH = 100      # If not detected automatically
