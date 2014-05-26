#!/usr/bin/env python2.7

"""

Written by benaryorg (@benaryorg/binary@benary.org)
Given away in peace!

License: WTFPL (see LICENSE file of git.benary.org/PyBuecherverwaltung)

"""

import re

class Buch(object):
    bnrptrn=re.compile('[a-zA-Z]{3}\d{7}')

    def __init__(self,buchnummer,titel='',bestand=0,preis=0.0):
        if buchnummer==None:
            lst=titel.split(';')
            if len(lst)!=4:
                raise ValueError('Unparsable')
            self.buchnummer=str(lst[0])
            self.titel=str(lst[1])
            self.bestand=int(lst[2])
            self.preis=float(lst[3])
        else:
            self.buchnummer=str(buchnummer)
            self.titel=str(titel)
            self.bestand=int(bestand)
            self.preis=float(preis)
        if len(self.buchnummer)!=10 or not self.bnrptrn.match(self.buchnummer):
            raise ValueError('Booknumber has to be like AAA0000000')
        if self.bestand<0:
            raise ValueError('Count cannot be negative')
        if self.preis<0:
            raise ValueError('Price cannot be negative')

    def __hash__(self):
        return hash(self.buchnummer)

    def __add__(self,other):
        if type(other)==type(self) and other.buchnummer==self.buchnummer and other.titel==self.titel:
            return Buch(self.buchnummer,self.titel,self.bestand+other.bestand,other.preis)
        else:
            raise ValueError('Not addable')

    def __cmp__(self,other):
        if type(other)==type(self):
            return cmp(self.buchnummer,other.buchnummer)
        raise TypeError('Cannot compare Book with %s'%str(type(other)))

    def __str__(self):
#        return ';'.join([self.buchnummer,self.titel,str(self.bestand),str(self.preis)])
        return self.__repr__()

    def __repr__(self):
        return '%s %50s | %5d*%4.2f'%(self.buchnummer,self.titel,self.bestand,self.preis)

    @staticmethod
    def createSet(fname,data=None,verbose=False):
        buecher=set(data) if data else set()
        with open(fname) as f:
            while True:
                s=f.readline()[:-1]
                if s==None or s=='':
                    break
                try:
                    b=Buch(None,s)
                    if b not in buecher:
                        buecher.add(b)
                    else:
                        for b2 in buecher:
                            if hash(b2)==hash(b):
                                b=b2+b
                                buecher.remove(b)
                                buecher.add(b)
                except ValueError,ex:
                    if verbose:
                        print ex
        return buecher

    @staticmethod
    def saveTo(fname,buecher,verbose=False):
        if verbose:
            print 'Writing %d Books to "%s"'%(len(buecher),fname)
        with open(fname,'w') as f:
            for b in buecher:
                f.write(';'.join([b.buchnummer,b.titel,str(b.bestand),str(b.preis)])+"\n")
