#!/usr/bin/env python

""" The command line for now, the logic should later be factored out to be
importable in sublime plugin

"""

import os
import sys

DOXELS_REPO = '/Users/kamrik/src/dox/doxels'


class Doxel():
    def __init__(self, title=None, body='', props={}):
        self.title = title
        self.body = body
        self.props = props

        # TODO: id should the id withing the repo, not including path to the
        # root of the repo. Loading a doxel should probably be a method or
        # the Repo class. and fromfile() should become fromlines()
        self.id = None

    def __repr__(self):
        """For now we use filepath cause we
        """
        s = 'Doxel: ' + self.id
        return s

    @classmethod
    def fromfile(cls, filepath):
        title = None
        propLines = []
        bodyLines = []

        with open(filepath, encoding='UTF-8') as f:
            for line in f:
                line = line.strip()
                # if it's an empty line, ignore it
                if not line:
                    continue
                # A line that starts with a dot is a line of properties
                if line.startswith('.'):
                    propLines.append(line)
                    continue

                # This is non empty line that doesn't start with a dot If we still
                # don't have a title, it's first such line, use it as title.
                if not title:
                    title = line
                    continue

                # Not title, not props -> body
                bodyLines.append(line)
        # End of for line in file

        body = '\n'.join(bodyLines)
        props = parse_props(propLines)
        d = cls(title, body, props)
        d.id = filepath
        return d


class Repo():
    def __init__(self, path):
        self.path = path
        self.read_repo()

    def read_repo(self):
        """ Walk the dir and read all doxel files """
        doxels = []
        for dirinfo in os.walk(DOXELS_REPO):
            for fname in dirinfo[2]:
                if fname.lower().endswith('.doxel'):
                    d = Doxel.fromfile(os.path.join(dirinfo[0], fname))
                    doxels.append(d)

        self.doxels = doxels

    def __len__(self):
        return len(self.doxels)

    def query(self, qry):
        """
        Simplest query:
        tag1 tag2 = tag1 and tag2 are both truthy

        TODO: Add some real lang
            python? (indexability)
            some lib parsing local predicates?
        """
        tags = qry.strip().split()
        res = [d for d in self.doxels if all(t in d.props for t in tags)]
        return res

# End of class Repo


def maybe_convert(x):
    try:
        y = int(x)
    except ValueError:
        try:
            y = float(x)
        except ValueError:
            y = x
    return y


def parse_props(propLines):
    """ Replace this with something real, this is lame

    What about data types? Especially dates?
    Should we convert when parsing.
    Better to convert when querying. Then
    Should it be
    .deadline = time(2014-05-06)
    or should the presence of work date or time in the name imply type?

    Anyway, for now anything is string or number if it looks like a number

    """
    props = {}
    for line in propLines:
        tokens = [t.strip().strip('.') for t in line.split()]
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '=':
                props[tokens[i-1]] = maybe_convert(tokens[i+1])
                i += 2
            else:
                props[token] = True
                i += 1

    return props


if __name__ == "__main__":
    repo = Repo(DOXELS_REPO)
    print(len(repo.doxels))
    print(os.path.dirname(__file__))
    print(sys.version)
    print('\n'.join(d.id for d in repo.query('todo')))

    # filepath = '/Users/kamrik/src/dox/doxels/GioraFeidman_Clarinet.doxel'
    # d = Doxel.fromfile(filepath)
    # print(d.title)

    #props = parse_props(['.zetag .foo = bar'])
    #print(props)
