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
""" USB command object """
from __future__ import unicode_literals

import FreeCAD
from App import Script

if FreeCAD.GuiUp:
    import FreeCADGui


class CommandPool:

    def GetResources(self):
        return {b"Pixmap"   : b"icons:Usb-Pool.xpm",
                b"MenuText" : b"New Pool",
                b"Accel"    : b"U, N",
                b"ToolTip"  : b"New Pool",
                b"Checkable": True}

    def IsActive(self):
        return True

    def Activated(self, index):
        if FreeCAD.ActiveDocument is None:
            FreeCAD.newDocument()
        FreeCAD.ActiveDocument.openTransaction(b"New Pool")
        code = '''from App import UsbPool
from Gui import UsbPoolGui, PySerialGui
obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "Pool")
UsbPool.Pool(obj)
UsbPoolGui._ViewProviderPool(obj.ViewObject)'''
        FreeCADGui.doCommand(code)
        FreeCAD.ActiveDocument.commitTransaction()
        FreeCAD.ActiveDocument.recompute()


class CommandRefresh:

    def GetResources(self):
        return {b"Pixmap"  : b"icons:Usb-Refresh.xpm",
                b"MenuText": b"Refresh port",
                b"Accel"   : b"U, R",
                b"ToolTip" : b"Refresh available port"}

    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            s = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)
            if len(s):
                obj = s[0]
                if Script.getObjectType(obj) == "App::UsbPool" or\
                   Script.getObjectType(obj) == "App::PySerial":
                    return True
        return False

    def Activated(self):
        obj = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)[0]
        code = '''obj = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)[0]\n'''
        if Script.getObjectType(obj) == "App::UsbPool":
            code += '''for o in obj.Serials:
    o.Proxy.Update = ["Port", "Baudrate"]
    o.touch()'''
        if Script.getObjectType(obj) == "App::PySerial":
            code += '''obj.Proxy.Update = ["Port", "Baudrate"]
obj.touch()'''
        FreeCADGui.doCommand(code)
        FreeCAD.ActiveDocument.recompute()


class CommandOpen:

    def GetResources(self):
        return {b"Pixmap"  : b"icons:Usb-Terminal.xpm",
                b"MenuText": b"Open Terminal",
                b"Accel"   : b"U, T",
                b"ToolTip" : b"Connect/disconnect terminal"}

    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            s = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)
            if len(s):
                obj = s[0]
                if Script.getObjectType(obj) == "App::PySerial" and\
                   obj.Proxy.hasParent(obj) or\
                   Script.getObjectType(obj) == "App::UsbPool":
                    return True
        return False

    def Activated(self):
        obj = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)[0]
        code = '''obj = Gui.Selection.getSelection(App.ActiveDocument.Name)[0]\n'''
        if Script.getObjectType(obj) == "App::PySerial":
            obj = obj.Proxy.getParent(obj)
            code += '''obj = obj.Proxy.getParent(obj)\n'''
        if obj.Proxy.Machine.isRunning():
            code += '''obj.Proxy.Machine.stop()'''
        else:
            code += '''obj.Proxy.Machine.start(obj)'''            
        FreeCADGui.doCommand(code)
        FreeCAD.ActiveDocument.recompute()


class CommandStart:

    def GetResources(self):
        return {b"Pixmap"  : b"icons:Usb-Upload.xpm",
                b"MenuText": b"File upload",
                b"Accel"   : b"U, F",
                b"ToolTip" : b"Start/stop file upload"}

    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            s = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)
            if len(s):
                obj = s[0]
                if Script.getObjectType(obj) == "App::PySerial":
                    obj = obj.Proxy.getParent(obj)                
                if Script.getObjectType(obj) == "App::UsbPool" and\
                   obj.Proxy.Machine.run:
                    return True
        return False

    def Activated(self):
        obj = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)[0]
        code = '''obj = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)[0]\n'''
        if Script.getObjectType(obj) == "App::UsbPool":
            code += '''obj.Start = not obj.Start'''
        if Script.getObjectType(obj) == "App::PySerial":
            code += '''obj.InList[0].Start = not obj.InList[0].Start'''
        FreeCADGui.doCommand(code)
        FreeCAD.ActiveDocument.recompute()


class CommandPause:

    def GetResources(self):
        return {b"Pixmap"  : b"icons:Usb-Pause.xpm",
                b"MenuText": b"Pause file upload",
                b"Accel"   : b"U, P",
                b"ToolTip" : b"Pause/resume file upload"}

    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            s = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)
            if len(s):
                obj = s[0]
                if (Script.getObjectType(obj) == "App::UsbPool" and obj.Start) or\
                   (Script.getObjectType(obj) == "App::PySerial" and obj.InList[0].Start):
                    return True
        return False

    def Activated(self):
        obj = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)[0]
        code = '''obj = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Name)[0]\n'''
        if Script.getObjectType(obj) == "App::UsbPool":
            code += '''obj.Pause = not obj.Pause'''
        if Script.getObjectType(obj) == "App::PySerial":
            code += '''obj.InList[0].Pause = not obj.InList[0].Pause'''
        FreeCADGui.doCommand(code)
        FreeCAD.ActiveDocument.recompute()


if FreeCAD.GuiUp:
    # register the FreeCAD command
    FreeCADGui.addCommand("Usb_Pool", CommandPool())
    FreeCADGui.addCommand("Usb_Refresh", CommandRefresh())
    FreeCADGui.addCommand("Usb_Open", CommandOpen())
    FreeCADGui.addCommand("Usb_Start", CommandStart())
    FreeCADGui.addCommand("Usb_Pause", CommandPause())

FreeCAD.Console.PrintLog("Loading UsbCommand... done\n")
