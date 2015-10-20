# -*- coding: utf-8 -*-

#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2015 Pierre Vacher <prrvchr@gmail.com>                  *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************
""" TinyG2 panel Plugin object """
from __future__ import unicode_literals

import FreeCADGui
from PySide import QtGui


class UsbPoolPanel:

    def __init__(self, pool):
        self.form = UsbPoolTaskPanel(pool)

    def accept(self):
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def reject(self):
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def clicked(self, index):
        pass

    def open(self):
        pass

    def needsFullSpace(self):
        return False

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)
        #return int(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)

    def helpRequested(self):
        pass


class UsbPoolTaskPanel(QtGui.QGroupBox):

    def __init__(self, pool):
        QtGui.QGroupBox.__init__(self)
        self.setObjectName("TinyG2-Monitor")
        self.setWindowTitle("TinyG2 Monitor")
        self.setWindowIcon(QtGui.QIcon("icons:Usb-Pool.xpm"))
        layout = QtGui.QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        if not pool.Start:
            txt = QtGui.QLabel("More information while upload!!!")
            layout.addWidget(txt, 0, 0, 1, 1)
            return
        layout.addWidget(QtGui.QLabel("Line:"), 0, 0, 1, 1)
        line = QtGui.QLabel()
        layout.addWidget(line, 0, 1, 1, 3)
        pool.Process.uploader.line.connect(line.setText)
        layout.addWidget(QtGui.QLabel("GCode:"), 1, 0, 1, 1)
        gcode = QtGui.QLabel()
        layout.addWidget(gcode, 1, 1, 1, 3)
        pool.Process.uploader.gcode.connect(gcode.setText)
        layout.addWidget(QtGui.QLabel("Buffers:"), 2, 0, 1, 1)
        buffers = QtGui.QLabel()
        layout.addWidget(buffers, 2, 1, 1, 3)
        pool.Process.reader.freebuffer.connect(buffers.setText)
        layout.addWidget(QtGui.QLabel("PosX:"), 3, 0, 1, 1)
        posx = QtGui.QLabel()
        layout.addWidget(posx, 3, 1, 1, 3)        
        pool.Process.pointx.connect(posx.setText)
        layout.addWidget(QtGui.QLabel("PosY:"), 4, 0, 1, 1)        
        posy = QtGui.QLabel()
        layout.addWidget(posy, 4, 1, 1, 3)        
        pool.Process.pointy.connect(posy.setText)
        layout.addWidget(QtGui.QLabel("PosZ:"), 5, 0, 1, 1)  
        posz = QtGui.QLabel()
        layout.addWidget(posz, 5, 1, 1, 3)        
        pool.Process.pointz.connect(posz.setText)
