#!/usr/bin/env python

import os
import re
import gettext

gettext.install('movie-namer')

def getdirtydirs():
    movies = []
    for l in sorted(filter(os.path.isdir, os.listdir(os.getcwd()))):
        match = re.search("^[^.]+? \[\d{4}\]$", l)
        if match is not None:
            continue
        movies.append(l)
    return movies


if __name__ == "__main__":
    print _('Movie Namer')
    print
    print _('Current Directory: {0}').format(os.getcwd())
    print
    
    movies = getdirtydirs()
    
    if not len(movies) == 1:
        print _('{0!s} dirty directories found').format(len(movies))
    else:
        print _('1 dirty directory found')
