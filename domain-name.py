#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from optparse import OptionParser

CONFIG = '/etc/bind/named.conf.slave'
#CONFIG = './named.conf.slave'

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
    return True if os.path.isfile(DOMAINS_FOLDER + domain) else Flase

def add(domain):
    if exist(domain):
	print('Домен ' + domain + ' уже был добавлен')
    else:
        add_block = '''

zone "''' + domain + '''" IN {
        type slave;
        file "''' + DOMAINS_FOLDER + domain + '''";
        masters { ''' + MASTER_NS + '''; };
};'''
        s = str(add_block)
        f = open(CONFIG, 'a')
        f.write(s)
	print('Домен ' + domain + ' добавлен')

def add_mass(filename):
    for domain in open(filename):
	add(domain.replace('\n','',))

# ^-- Deprecated since version 2.7
#import argparse
#parser = argparse.ArgumentParser(description='Скрипт для добавления www доменов.')

def main():
    p = OptionParser(usage="%prog [опции] [файл|домен]", version="%prog 0.2")
    p.add_option('-a','--add',dest='domain',
		 help='Домен для добавления')
    p.add_option('-m','--mass',dest='filename',
		 help='Файл для массового добавления доменов')
    (options, args) = p.parse_args()
    domain = options.domain if options.domain else None
    filename = options.filename if options.filename else None
    #print('проверка\n'+filename)


#if len(sys.argv) > 1:
#    try:
#        if sys.argv[1] in ('-h','-help','--help'):
#            hlp()
#        elif sys.argv[1] == '-add':
#            add(sys.argv[2])
#        elif sys.argv[1] == '-mass':
#            add_mass(sys.argv[2])
#            print('\nМассовое добавление завершено')
#    except IndexError:
#        hlp()
#else:
#    hlp()

#os.system('rndc reload')
if __name__ == "__main__":
    main()
