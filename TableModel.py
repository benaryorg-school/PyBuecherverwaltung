from PyQt4.QtGui import *
from PyQt4.QtCore import *

"""

Written by benaryorg (@benaryorg/binary@benary.org)
Given away in peace!

License: WTFPL (see LICENSE file of git.benary.org/PyBuecherverwaltung)

"""

class TableModel(QAbstractTableModel): 

    def __init__(self,data,headers,parent=None,*largs):
        QAbstractTableModel.__init__(self,parent,*largs)
        self.arraydata=data
        self.headerdata=headers

    def rowCount(self,parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.headerdata)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role!=Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self,col,orientation,role):
        if orientation==Qt.Horizontal and role==Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

