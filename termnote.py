# -*-coding: utf-8 -*-
'''
Author:         Arijit Basu
Email:          sayanarijit@gmail.com
Documentation:  https://github.com/sayanarijit/termnote.py
'''

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import re
import os
import sys
from subprocess import call
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from collections import OrderedDict


# --------------------------------- CONFIG ---------------------------------- #

VERSION = 'v1.1.0'
EDITOR = os.environ.get('EDITOR', 'vi')
STORAGE = os.environ.get('TN_STORAGE', os.path.expanduser('~') + '/.termnote')
SCREEN_WIDTH = 100      # If not detected automatically

# --------------------------------------------------------------------------- #


try:
    _, columns = map(int, os.popen('stty size', 'r').read().split())
except:
    columns = SCREEN_WIDTH


def clr():
    """
    Keeps screen clean
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def interact(qry, options=[], default=None):
    """
    Interacts with user
    """
    qry = qry.decode() if hasattr(qry, 'decode') else qry
    if default is None: default = ''
    if hasattr(default, 'decode'): default = default.decode()
    options = list(map(str, options))
    completer = WordCompleter(options, ignore_case=True)
    # try:
    inp = prompt(qry, completer=completer, default=default)
    if inp:
        return inp
    else:
        quit()
    # except:
    #     quit()


def readfile(filename):
    """
    Reads file and returns its content
    """
    with open(os.path.join(STORAGE, filename)) as f:
        content = f.read()
    return content


def match_word(word, content):
    docwords = re.split('[^a-zA-Z0-9]', content.lower())
    return len([x for x in docwords if x.startswith(word)])


class TermNote:
    """
    Just the main class
    """
    def __init__(self):
        self.note = None
        self.searched = []
        self.found = OrderedDict()
        self.options = OrderedDict()
        self.allnotes = OrderedDict()
        self.allwords = []

    def new(self, title=None):
        clr()
        filename = interact('Enter title: ', default=title,
                            options=self.allwords)
        filepath = os.path.join(STORAGE, filename)

        while os.path.exists(filepath):
            clr()
            print('Note "{}" already exists!'.format(filename))
            filename = interact('Try another title: ',
                                default=filename, options=self.allwords)
            filepath = os.path.join(STORAGE, filename)

        call([EDITOR, filepath])

        if os.path.isfile(filepath):
            self.note = filename
        else:
            print('No new file created...!')
            quit()

    def scandir(self):
        if not os.path.isdir(STORAGE): os.makedirs(STORAGE)
        allfilenames = [f for f in os.listdir(STORAGE) if os.path.isfile(STORAGE+'/'+f)]
        allcontents = [readfile(f) for f in allfilenames]
        self.allwords = []
        self.allnotes = OrderedDict()
        for x in allcontents + allfilenames:
            self.allwords.extend(re.split('[^a-zA-Z0-9]', x))
        self.allwords = list(set(self.allwords))
        if '' in self.allwords: self.allwords.remove('')
        self.allnotes = OrderedDict(zip(allfilenames, allcontents))

    def search_or_select(self, entered=None):
        self.scandir()
        if entered is None:
            entered = interact(
                'Search or select: ',
                options=list(self.options.keys()) + list(self.found.keys()) + self.allwords
            )
        if entered.isnumeric() and int(entered) in self.found:
            self.note = self.found[int(entered)]
            return
        if entered in self.options:
            getattr(self, self.options[entered])()
            return
        self.searched = entered.split()
        match_count = {
            k: sum([match_word(w, k+' '+v) for w in self.searched])
                for k,v in self.allnotes.items()
        }
        found = [k for k,v in match_count.items() if v != 0]
        self.found = OrderedDict(enumerate(
            sorted(found, key=lambda x: match_count[x], reverse=True)
        ))
        if len(self.found) == 0:
            clr()
            print('No result found for "{}"...!\n'.format(entered))
            ans = interact('Create new note? [y/N]', options=['y', 'n'])
            if ans in ['y', 'Y']:
                self.new(entered)
        elif len(self.found) == 1:
            self.note = self.found[0]

    def display(self):
        clr()
        if self.note is not None:
            filepath = STORAGE + '/' + self.note
            print(('   '+self.note+'   ').center(columns, '='))
            print('\n'+readfile(filepath)+'\n')

            self.options = OrderedDict((
                ('e','edit'),
                ('r','rename'),
                ('d','delete'),
                ('b','back'),
                ('q','quit')
            ))
        else:
            print('Found total:',len(self.found))
            print(('='*columns)+'\n')
            if len(self.found) == 0:
                print('\n\n    No result found...!\n\n')
            for k,v in self.found.items():
                print('    {}) {}'.format(k, v))
            print()
            self.options = OrderedDict((
                ('n','new'),
                ('a','all'),
                ('h','help'),
                ('q','quit')
            ))
        print('-'*columns)
        print(('   '.join(
            ['{}) {}'.format(k,v) for k, v in self.options.items()]
        )).center(columns))
        print('-'*columns)

    def all(self):
        self.note = None
        self.found = OrderedDict(enumerate(self.allnotes.keys()))

    def edit(self):
        call([EDITOR, os.path.join(STORAGE, self.note)])

    def rename(self):
        clr()
        filename = interact('Enter title: ', default=self.note,
                            options=self.allwords)
        filepath = os.path.join(STORAGE, filename)

        while os.path.exists(filepath):
            clr()
            print('Note "{}" already exists!'.format(filename))
            filename = interact(
                'Try another title: ',
                default=filename,
                options=self.allwords
            )
            filepath = os.path.join(STORAGE, filename)

        os.rename(os.path.join(STORAGE, self.note), filepath)
        self.scandir()
        for k,v in self.found.items():
            if v == self.note:
                self.found[k] = filename
                break
        self.note = filename

    def delete(self):
        clr()
        ans = interact('Delete note "{}"? [ y/N ]: '.format(self.note),
                        options=['y', 'n'])
        clr()
        if ans in ['y', 'Y']:
            filepath = os.path.join(STORAGE, self.note)
            os.remove(filepath)
            if not os.path.isfile(filepath):
                print('Deleted file: "{}"'.format(filepath))
                quit()
        print('File not deleted...!')

    def back(self):
        if len(self.found) == 0:
            self.all()
        self.note = None

    def quit(self):
            quit()

    def help(self):
        print()
        print('Usage:\t\ttn KEYWORDS [e.g. tn patching rhel kernel]')
        print()
        quit()


def run():
    termnote = TermNote()
    if len(sys.argv) > 1:
        searched = ' '.join(sys.argv[1:])
        termnote.search_or_select(searched)
    else:
        termnote.scandir()
        termnote.all()
    while True:
        termnote.display()
        termnote.search_or_select()


if __name__ == '__main__':
    run()
