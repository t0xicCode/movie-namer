#!/usr/bin/env python

import os
import re
import gettext
import sys

gettext.install('movie-namer')

def getdirtydirs():
    movies = []
    for movie_dir in sorted(filter(os.path.isdir, os.listdir(os.getcwd()))):
        if re.search("^[^.]+? \[\d{4}\]$", movie_dir):
            continue
        movies.append(movie_dir)
    return movies

def getinfo(dirs):
    info = {}
    for movie_dir in dirs:
        print
        print _('Directory: {0}').format(movie_dir)
        if raw_input(_('Please choose (C)ontinue, (S)kip: ')) == _('s'):
            continue
        name = year = ''
        while True:
            if name is '':
                name_match = re.search("(.+).[[({]?\d{4}", movie_dir)
                if name_match:
                    name = name_match.group(1).strip().replace('.', ' ').title()
            tmp = raw_input(_('Name ({0}): ').format(name))
            name = tmp if tmp is not '' else name
            if year is '':
                year_match = re.search("(\d{4})", movie_dir)
                if year_match:
                    year = year_match.group(1)
            tmp = raw_input(_('Year ({0}): ').format(year))
            year = tmp if tmp is not '' else year
            if raw_input(_('Renaming to \'{0} [{1!s}]\'. OK(Y/n)? ').format(name, year)) is not _('n'):
                info[movie_dir] = '{0} [{1!s}]'.format(name, year)
                break
    return info

def rename(old, new):
    result = False
    print _('    {0} --> {1}').format(old, new)
    print _('        {0}').format('OK' if result else 'FAIL')
    return result

def main():
    print _('Movie Namer')
    print
    print _('Current Directory: {0}').format(os.getcwd())
    print
    
    movies = getdirtydirs()
    
    if len(movies) is 0:
        print _('Nothing to rename')
        sys.exit(0)
    
    if len(movies) is not 1:
        print _('{0!s} dirty directories found').format(len(movies))
    else:
        print _('1 dirty directory found')
    
    renames = getinfo(movies)
    
    if len(renames) is 0:
        print _('Nothing to rename')
        sys.exit(0)
    
    print
    print _('Renaming')
    for old, new in renames.iteritems():
        rename(old, new)

if __name__ == "__main__":
    main()
