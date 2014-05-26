#!/usr/bin/env python2.7

"""

Written by benaryorg (@benaryorg/binary@benary.org)
Given away in peace!

License: WTFPL (see LICENSE file of git.benary.org/PyBuecherverwaltung)

"""

from TableModel import TableModel
from Buch import Buch
from PyQt4.QtGui import *

class MainWindow(QMainWindow):
    
    modified=False

    def __init__(self,args,data):
        super(MainWindow,self).__init__()
        if args.verbose:
            print 'Initialising Window'
        self.args=args
        self.data=data
        self.title='Main Window'
        self.initUi()
        self.statusBar().showMessage('Ready')
        if args.verbose:
            print 'Main Window Ready'

    def initUi(self):
        self.resize(640,400)

        menubar=self.menuBar()
        filemenu=menubar.addMenu('&File')

        action=filemenu.addAction('&Open')
        action.setShortcut('Ctrl+O')
        action.setStatusTip('Open File')
        action.triggered.connect(self.open)

        action=filemenu.addAction('&Save')
        action.setShortcut('Ctrl+S')
        action.setStatusTip('Save Data')
        action.triggered.connect(self.save)

        action=filemenu.addAction('S&ave as...')
        action.setShortcut('Ctrl+Shift+S')
        action.setStatusTip('Save Data to File ...')
        action.triggered.connect(self.saveAs)

        action=filemenu.addAction('&Add')
        action.setStatusTip('Add File')
        action.triggered.connect(self.add)

        action=filemenu.addAction('&Quit')
        action.setShortcut('Ctrl+Q')
        action.setStatusTip('Exit application')
        action.triggered.connect(self.quit)

        self.retranslateUi()
    
    def createTable(self):
        tv=QTableView()
        l=list(self.data)
        l.sort(lambda b1,b2:cmp(b1.buchnummer,b2.buchnummer))
        tm=TableModel(list((b.buchnummer,b.titel,b.bestand,'%.2f'%b.preis) for b in l),['Buchnummer','Titel','Bestand','Preis'])
        tv.setModel(tm)
        tv.setShowGrid(False)
        vh=tv.verticalHeader()
        vh.setVisible(False)
        hh=tv.horizontalHeader()
        hh.setStretchLastSection(True)
        tv.resizeColumnsToContents()
        for row in xrange(len(self.data)):
            tv.setRowHeight(row,18)
        return tv

    def retranslateUi(self):
        self.setWindowTitle(self.title)
        self.setCentralWidget(self.createTable())

    def open(self,*largs):
        if self.args.verbose:
            print 'Open a File'
        fname=self.chooseFile()
        if fname:
            self.data=Buch.createSet(fname,verbose=self.args.verbose)
            self.modified=False
            self.args.filename=fname
            self.retranslateUi()
            
    def save(self,*largs):
        if self.args.verbose:
            print 'Save to %s'%self.args.filename
        Buch.saveTo(self.args.filename,self.data,verbose=self.args.verbose)
        self.modified=False

    def saveAs(self,*largs):
        if self.args.verbose:
            print 'Save as File'
        fname=self.chooseFile()
        if fname:
            Buch.saveTo(fname,self.data,verbose=self.args.verbose)
            self.args.filename=fname
            self.modified=False

    def add(self,*largs):
        if self.args.verbose:
            print 'Add a File'
        fname=self.chooseFile()
        if fname:
            self.data=Buch.createSet(fname,data=self.data,verbose=self.args.verbose)
            self.modified=True
            self.retranslateUi()

    def chooseFile(self):
        fname=QFileDialog.getOpenFileName()
        if self.args.verbose:
            print 'File: "%s"'%fname
        return fname

    def closeEvent(self,event):
        event.ignore()
        self.quit()

    def quit(self):
        if self.modified:
            res=QMessageBox.question(self,'Save?','Do you want to save before quitting?',QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if res==QMessageBox.Cancel:
                return
            elif res==QMessageBox.Yes:
                self.save()
        qApp.quit()

