# TermNote

A simple, yet powerful and handy terminal based note taking python app


### Requirement:

* requires python (>2 or 3)


### Usage:

* Install with pip

```
sudo pip install termnote
```

Note: For the sake of LAZYNESS, 'tn' is a shortcut for 'termnote'

* Create your 1st note

```
tn my first note
```

* Write "I love cheeze" and close editor. Note is created. Now lets find the note by keywords

```
tn cheez
```

or by filename

```
tn first no
```

* List all notes

```
tn
```


### Customization

You can change default editor and path by adding below lines in your '~/.profile' file

```
export EDITOR="[Your favourite text editor. Default is 'vi']"
export TN_STORAGE="[Directory where notes to be saved. Default is '~/.termnote']"
```
