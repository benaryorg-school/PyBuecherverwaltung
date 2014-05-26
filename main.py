#!/usr/bin/env python2.7

"""

Written by benaryorg (@benaryorg/binary@benary.org)
Given away in peace!

License: WTFPL (see LICENSE file of https://git.benary.org/PyBuecherverwaltung)

"""

import sys
from Buch import Buch
from argparse import ArgumentParser
from PyQt4.QtGui import QApplication
from MainWindow import MainWindow

if __name__=='__main__':
    parser=ArgumentParser(description='A Program for managing Books')
    parser.add_argument('-v','--verbose',action='store_true',dest='verbose',default=False,help='Verbose Output')
    parser.add_argument('-t','--text','--nogui',action='store_false',dest='gui',default=True,help='Do not show Grafical User Interface')
#    parser.add_argument('-f','--file',dest='filename',help='File to load',metavar='FILE')
    parser.add_argument(dest='filename',nargs='?',help='File to load',metavar='FILE')

    args=parser.parse_args()
    
    buecher=set()
    if args.filename:
        buecher=Buch.createSet(args.filename,verbose=args.verbose)
    if args.gui:
        app=QApplication(sys.argv)
        win=MainWindow(args,buecher)
        win.show()
        sys.exit(app.exec_())
    else:
        for buch in buecher:
            print buch
        s=''
        while s.lower()!='quit':
            try:
                s=raw_input('> ')
            except EOFError,ex:
                s='quit'
                print s

