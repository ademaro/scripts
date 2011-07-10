#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, time
from datetime import date
from optparse import OptionParser, Option

# Complete hack.
Option.ALWAYS_TYPED_ACTIONS += ('callback',)


CONFIG = '/etc/bind/named.conf.slave'
#CONFIG = './named.conf.slave'

NOW = date.today()

DOMAINS_FOLDER = '/etc/bind/slave/'

MASTER_NS = '194.105.194.141'

def hlp():
    print('''Usage: [function] [parameters]
      [function]
        -add domain - to add domain in bind9
        -mass filename - to add domains from filename
Examples:
     add-domain-name.py -add pixelon.ru
     add-domain-name.py -mass filename
                       ''')

def exist(domain):
    if os.path.isfile(DOMAINS_FOLDER + domain): return True
    else: return False

def add(option, opt_str, domain, parser):
    for line in open(CONFIG):
        if domain in line:
            print('Domain ' + domain + ' already in config')
            return False
    if exist(domain):
        print('Domain ' + domain + ' already added')
        return False

    add_block = '''

zone "''' + domain + '''" IN {
        type slave;
        file "''' + DOMAINS_FOLDER + domain + '''";
        masters { ''' + MASTER_NS + '''; };
};'''
    s = str(add_block)
    f = open(CONFIG, 'a')
    f.write(s)
    print('Domain ' + domain + ' added')

def domdelete(option, opt_str, domain, parser):

    os.system('cp '+CONFIG+' '+CONFIG+'.'+str(NOW))
    domfile = open(CONFIG+'.'+str(NOW), "r")
    start = -1
    f = open(CONFIG, 'w')
    for line in domfile:
           if (line.replace('\n','',) == 'zone "' + domain + '" IN {'):
              start = 0
           if start>=0:
              start = start + 1
           else:
              f.write(line)
           if start > 5:
              start = -1
              if not exist(domain):
                  print('Domain file ' + domain + ' not found')
              else:
                  os.system("unlink "+DOMAINS_FOLDER + domain)
              print('Domain ' + domain + ' deleted')
    if start>=0:
              if not exist(domain):
                  print('Domain file ' + domain + ' not found')
              else:
                  os.system("unlink "+DOMAINS_FOLDER + domain)
              print('Domain ' + domain + ' deleted')

    domfile.close()
    f.close()


def add_mass(option, opt_str, filename, parser):
    for domain in open(filename):
        add('','',domain.replace('\n','',),'')

def delete_mass(option, opt_str, filename, parser):

    for domain in open(filename):
        domdelete('','',domain.replace('\n','',),'')

#from optparse import OptionParser
#parser = OptionParser()
#parser.add_option("-h", "--help", help="write report to FILE", metavar="FILE")

# ^-- Deprecated since version 2.7
#import argparse
#parser = argparse.ArgumentParser(description='Скрипт для добавления www доменов.')

def main():
    return  0

#    domain = string(options.domain) if options.domain else None

#    print(options)
#    keys = sorted(options.keys())
#    for opk in options:
#       if(options[opk]):
#        print opk + ' = '
       
#else:
#    hlp()

#os.system('rndc reload')
global options
global args

p = OptionParser(usage="Usage: %prog [options] [file|domain]", version="%prog 0.2")

p.add_option('-a','--add',action='callback',dest='domain', type='string',  callback=add,
                 help='Domain to add')
p.add_option('-m','--mass',action='callback',dest='filename', type='string',  callback=add_mass,
                 help='File to mass add domains')
p.add_option('-d','--delete',action='callback',  dest='domain', type='string',  callback=domdelete,
                 help='Domain to delete')
p.add_option('-n','--massdel',action='callback',  dest='filename', type='string',  callback=delete_mass,
                 help='File to mass delete')
(options, args) = p.parse_args()
if __name__ == "__main__":
    main()