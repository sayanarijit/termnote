#!/usr/bin/env python
# -*-coding: utf-8 -*-
'''
Author:         Arijit Basu
Email:          sayanarijit@gmail.com
Documentation:  https://sayanarijit.github.io/note.py
'''

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import os
import sys
import subprocess
from codecs import open
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from collections import OrderedDict


# Configuration -------------------------------------------------------------

VERSION = 'v1.0.5'
EDITOR = os.environ.get('EDITOR', 'vi')
STORAGE = os.environ.get('TN_STORAGE', os.path.expanduser('~') + '/.termnote')
SCREEN_WIDTH = 100 # If not detected automatically

#----------------------------------------------------------------------------


found, docs = None, None
try:
    _, columns = map(int, os.popen('stty size', 'r').read().split())
except:
    columns = SCREEN_WIDTH


def scan_dir():
    if not os.path.isdir(STORAGE): os.makedirs(STORAGE)
    filenames = [f for f in os.listdir(STORAGE) if os.path.isfile(STORAGE+'/'+f)]
    contents = list(map(readfile, filenames))
    return dict(zip(filenames, contents))


def clr():
    os.system('cls' if os.name == 'nt' else 'clear')


def interact(qry, options=[]):
    qry = qry.decode() if hasattr(qry, 'decode') else qry
    completer = WordCompleter(options, ignore_case=True)
    try:
        inp = prompt(qry, completer=completer)
        if inp:
            return inp
        else:
            quit()
    except:
        quit()

def select(choices):
    print('-'*columns)
    print(('   '.join([k+') '+v for k, v in choices.items() if type(k) != int])).center(columns))
    print('-'*columns)
    return interact('Search or select: ', options=list(choices.keys()))


def create_note(filename=None):
    clr()
    if not filename: filename = interact('Enter title: ')
    filepath = STORAGE + '/' + filename

    while os.path.exists(filepath):
        clr()
        print('Note "{}" already exists!'.format(filename))
        newname = interact('Try another title: ')
        filename = ' '.join(newname)
        filepath = STORAGE + '/' + filename

    subprocess.call([EDITOR, filepath])

    if os.path.isfile(filepath):
        display_note(filename)
    else:
        print('No new file created!')
        quit()


def display_note(filename):
    clr()
    global docs
    global found
    filepath = STORAGE + '/' + filename
    print(('   '+filename+'   ').center(columns, '='))
    print('\n'+readfile(filename)+'\n')

    choices = OrderedDict((('o','open with '+EDITOR), ('r','rename'),
               ('d','delete'), ('b','back'), ('q','quit')))

    try: found
    except: choices.pop('b')
    ans = select(choices).lower()

    if ans == 'o':
        subprocess.call([EDITOR, filepath])
        display_note(filename)
    elif ans == 'r':
        clr()
        newname = interact('Enter new title: ')
        while os.path.exists(STORAGE+'/'+newname):
            clr()
            print('Note "{}" already exists!'.format(filename))
            newname = interact('Try another title: ')

        os.rename(filepath, STORAGE+'/'+newname)
        display_note(newname)
    elif ans == 'd':
        clr()
        ans = interact('Delete file \''+filepath+'\'? [ y/N ]: ')
        clr()
        if ans in ['y','Y']:
            os.remove(filepath)
        if not os.path.isfile(filepath):
            print('Deleted file: "{}"'.format(filepath))
            quit()
        print('File not deleted!')
        quit()
    elif ans == 'b':
        display_search(found)
    elif ans == 'q':
        quit()
    else:
        found = search(ans.split())
        display_search(found, ans)


def display_help():
    print()
    print('Usage:\t\ttn KEYWORDS [e.g. tn patching rhel kernel]')
    print()
    quit()


def match_word(word, content):
    content = content.replace('\n',' ').replace('\r',' ').replace('\t',' ')
    return list(map(lambda x: word in x.lower(), content.lower().split())).count(True)


def readfile(filename):
    with open(STORAGE+'/'+filename, encoding='utf-8') as f:
        content = f.read()
    return str(content)


def search(words=[]):
    global docs
    global found
    match_count = {k: sum([match_word(w, k+' '+v) for w in words]) for k,v in docs.items()}
    found = [k for k,v in match_count.items() if v != 0]
    return sorted(found, key=lambda x: match_count[x], reverse=True)


def display_search(result, qry=None):
    clr()
    global docs
    if len(result) == 0 and qry:
        print('No match found...')
        ans = interact('Create new note with title "{}"? [y/N]: '.format(qry)).lower()
        if ans == 'y':
            create_note(qry)
        return

    print('Found total:',len(result))
    print('='*columns)
    i = 1

    print()
    notes = {}
    for filename in result:
        print('    '+str(i)+')', filename)
        notes[str(i)] = filename
        i+= 1
    print()

    choices = OrderedDict((('n','new note'), ('a','list all'), ('h','help'), ('q','quit')))
    ans = select(choices)
    if ans in list(map(str, range(1,len(result)+1))):
        display_note(notes[ans])
    elif ans == 'a':
        display_search(docs.keys())
    elif ans == 'q':
        quit()
    elif ans == 'h':
        display_help()
    elif ans == 'n':
        create_note()
        docs = scan_dir()
    else:
        found = search(ans.split())
        display_search(found, ans)


def run():

    global found
    global docs

    clr()
    docs = scan_dir()

    if len(docs) == 0: create_note()

    if len(sys.argv) > 1:
        found = search(sys.argv[1:])
        display_search(found, qry=' '.join(sys.argv[1:]))
    else:
        found = docs.keys()
        display_search(found)


if __name__ == '__main__':
    run()
