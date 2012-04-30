#!/usr/bin/env python

import os
import re
import gettext
import sys

gettext.install('movie-namer')

movie_extensions = ['mov', 'avi', 'mkv', 'mp4', '3gp', 'wmv', 'flv', 'swf']
subs_extensions = [ 'srt', 'sub', 'ssa', 'txt', 'idx']

l1 = '   {0}'
l2 = l1.format(l1)
l3 = l2.format(l1)

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
        if raw_input(l1.format(_('Please choose (C)ontinue, (S)kip: '))) in [_('s'), _('S')]:
            continue
        name = year = ''
        while True:
            if name is '':
                name_match = re.search("(.+).[[({]?\d{4}", movie_dir)
                if name_match:
                    name = name_match.group(1).strip().replace('.', ' ').title()
            tmp = raw_input(l1.format(_('Name ({0}): ').format(name)))
            name = tmp if tmp is not '' else name
            if year is '':
                year_match = re.search("(\d{4})", movie_dir)
                if year_match:
                    year = year_match.group(1)
            tmp = raw_input(l1.format(_('Year ({0}): ').format(year)))
            year = tmp if tmp is not '' else year
            if raw_input(l1.format(_('Renaming to \'{0} [{1!s}]\'. OK(Y/n)? ').format(name, year))) not in [_('n'), _('N')]:
                info[movie_dir] = '{0} [{1!s}]'.format(name, year)
                break
    return info

def rename(old, new):
    print
    print '{0} --> {1}'.format(old, new)
    try:
        print l1.format(_('Moving directory'))
        os.rename(os.path.join(os.getcwd(), old), os.path.join(os.getcwd(), new))
    except OSError:
        print l1.format(_('FAIL'))
        return False
    file_list = sorted(filter(lambda f: os.path.isfile(os.path.join(os.getcwd(), new, f)), os.listdir(os.path.join(os.getcwd(), new))))
    try:
        print l1.format(_('Moving movie files'))
        for movie in file_list:
            name, ext = os.path.splitext(movie)
            if ext[1:] not in movie_extensions:
                continue
            name = '.'.join([new, ext[1:]])
            delete = False
            while os.path.exists(os.path.join(os.getcwd(), new, name)):
                print l2.format('{0} --> '.format(movie)) 
                name = raw_input(l3.format(_('{0} already exist. Please choose another (blank to delete): ').format(name)))
                if name is '':
                    delete = True
                    break
            if delete is not True:
                print l2.format('{0} --> {1}'.format(movie, name))
                os.rename(os.path.join(os.getcwd(), new, movie), os.path.join(os.getcwd(), new, name))
            else:
                print l2.format(_('Removing {0}').format(movie))
                os.remove(os.path.join(os.getcwd(), new, movie))
    except OSError:
        print l1.format(_('FAIL'))
        return False
    try:
        print l1.format(_('Moving subtitle files'))
        for sub in file_list:
            name, ext = os.path.splitext(sub)
            if ext[1:] not in subs_extensions:
                continue
            name = '.'.join([new, ext[1:]])
            delete = False
            while os.path.exists(os.path.join(os.getcwd(), new, name)):
                print l2.format('{0} --> '.format(sub)) 
                name = raw_input(l3.format(_('{0} already exist. Please choose another (blank to delete): ').format(name)))
                if name is '':
                    delete = True
                    break
            if delete is not True:
                print l2.format('{0} --> {1}'.format(sub, name))
                os.rename(os.path.join(os.getcwd(), new, sub), os.path.join(os.getcwd(), new, name))
            else:
                print l2.format(_('Removing {0}').format(sub))
                os.remove(os.path.join(os.getcwd(), new, sub))
    except OSError:
        print l1.format(_('FAIL'))
        return False
    print l1.format(_('OK'))
    return True

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
