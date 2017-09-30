#!/usr/bin/env python3

from __future__ import print_function

import sys
import os
import argparse
import random
import pickle
import time

'''
List maker

- Create generic objects; use temp names if need be
- If unnamed, ask for a name
- Check against existing names; new name, or same name/new type?
- Object has property list + append function
- Append new items

- Create sentence objects with words as props
- Create word objects with ? as props
- Run the lists through an RNN
- Compare the evolving RNN output with indepent parse ranking
  for preferred interpretation

Types of lists
- to do (generic) for x, y, z
- parts list
- events
- locations (cities, countries, etc.)
- business locations
  by type (restaurants, cafes, grocers, shoes, clothing, etc.)
- any entity by type
- any entity by location
- any entity by time (day, month, year)
- any entity by purpose
- any living entity by motivation
- desires
'''

# To Do
'''
- Add options to delete and modify properties
- Add logging context handle 
- Reliably save & read data XXX beware object format changes!
- Modify pickled items
- Define available actions
- Add function timers (as context handler?)
'''

fin   = 'listmaker.test'    # default input file
fdata = 'listmaker.pickle'  # default data file
flog  = 'listmaker.log'

filelist   = []
objects    = []  # Lister class instances
objects_d  = {}
proc_limit = 3   # limit in seconds
proc_dict  = {}  # process dictionary

actions = ['make to do list', 'parse sentence', 'categorize list items',
            'search', 'retrieve', 'request', 'count', 'summarize',
            'analyze', 'edit file', 'update database', 'notify', 
            'calendar', 'store']

data_feed_types = ['news', 'local files', 'database', 'csv', 'directory tree']

# expectation for result
# either we get something we expect... or we don't
# new value is novel => calls introspection()
# expected value will reinforce validity/relevance/certainty pararmeters
expect = ['r1', 'r2']
# example: walk a directory tree. does ls resturn new? of type dir or file?


class Lister(object):

    props = []
    propsd = {}
    version = 1

    def __init__(self, name=''):
        if not name:
            prefix = 'lister'
            self.name = self.mktmp_name(prefix)
        else:
            self.name = name
        self.iprops = []
        self.ipropsd = {}
        self.usage = []
        self.event_context = []
        self.env_context = []

    @staticmethod
    def mktmp_name(prfx='tmp'):
        i = random.randint(1000, 9999)
        prfx = prfx + repr(i)
        return prfx


def timer():

    '''Time processes and exit if proc_limit is reached.
       Exit process and log if timer threshold reached.
       Might want to have multiple limits for different process types.
       Allow process to fight for additional time/resources, subject to
       logarithmic damping.
    '''
    pass


def test():

    '''Test object creation.
    '''

    # create temp name
    t1 = Lister()
    print (t1.name)
    objects.append(t1)

    # name provided
    t2 = Lister('to do')
    print (t2.name)
    objects.append(t2)

    print (objects)
    save_data(objects)


def add_items():

    # Query: What is it?
    # If has name, then look up in lexicon
    obj = Lister()
    if obj.name[:6] == 'lister':
        # XXX  Generate input requests dynamically one day...
        n = input('What is it? Or what is it called? >>> ')
        obj.name = n
    # property addition
    print('Using %s object' % obj.name)
    prop = None
    while 1:
        #prop = raw_input('Enter a property (None to quit.) >> ')
        prop = input('Enter a property (None to quit.) >> ')

        if prop:
            obj.iprops.append(prop)
        else:
            break
    
    # save data currently expects a list
    print ( type(obj) )
    save_data( [obj] )


# Ask What? => to identify properties; define
def what(x):
    pass


def parse_line(s):
    print ('parse_line:')
    pass1 = s.split()
    return pass1


def read_input(infile):
    with open(infile, 'r') as f3:
        for line in f3.readlines():
            linelist = parse_line(line)
            # inspect each word
            for item in linelist:
                if item in objects:
                    # if item exists; skip, or add new sense
                    # XXX sense detection still to come...
                    print ('skipping %s' % item)
                    continue
                w = Lister(item)
                print ('  %s' % w.name)
                # append sentence to track context
                # XXX need to limit context store and have prune() method
                # XXX also need to run RNN on usage context
                w.usage.append(line)
                objects.append(w)

                save_data(objects)


def read_data(datafile):
    # Assumes a stream of pickled objecs
    data = []
    with open(datafile, 'rb') as f4:
        while 1:
            try:
                rec = pickle.load(f4)
                data.append(rec)
            except EOFError:
                print ('... Read %s records.' % len(data))
                break
        
        return data


def save_data(obj_list):

    with open(fdata, 'ab+') as f:
        for x in obj_list:
            pickle.dump(x, f, 2)


def bkup_data():
    SRC = fdata
    TRGT = fdata + '_bak'
    # XXX if TRGT exists, compare digest with SRC file
    # XXX ...and skip the backup process the digests match.
    with open(TRGT, 'wb+') as f:
        try:
            os.system('cp SRC TRGT')
            print ('Success: data file copied to %s' % TRGT)   
        except:
            print ('Error: failed to backup data file.')


def main(args):

    if args.read:
        if args.filespec:
            print ('Warning: using -r flag; second filespec %s ignored.' % args.filespec)
        objects = read_data(args.read)
        #print (objects)
        for obj in objects:
            print (obj.name)
            for p in obj.iprops:
                oprop = str(obj.__dict__.get(p))
                print ('%s: %s' % (p, oprop))
                #print ('%s: '% p)
                #print (obj.__dict__)
        sys.exit()

    if args.test:
        if args.filespec:
            print ('Warning: using -t flag; filespec %s ignored.' % args.filespec)
        test()
        sys.exit()

    if args.filespec:
        # if input file provided, read and parse it...
        read_input(args.filespec)
    else:
        # otherwise, interactively add new items
        add_items()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
             description='Read input file and parse sentences into word objects.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--read', help='Read saved data file then quit.')
    group.add_argument('-t', '--test', action='store_true', help='Run tests then quit.')
    parser.add_argument('filespec', nargs='?', help='Read input from file line by line.')
    args = parser.parse_args()
    #print (args)  # prints Namespace
    main(args)
