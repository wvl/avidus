#
# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Original Code is  Avidus.
#
# The Initial Developer of the Original Code is Wayne Larsen.  
# Portions created by Wayne Larsen are
# Copyright (C) 2000.  All Rights Reserved.
#
# Contributor(s):
#

import sys
import math
from qt import *

class StyleComboItem(QListBoxPixmap):
    def __init__(self, listbox, n, h):
        QListBoxPixmap.__init__(listbox, n)
        self.highl = QPixmap(h)

    def __init__(self, n, h):
        QListBoxPixmap.__init__(self, n)
        self.highl = QPixmap(h)

    def paint(self, p):
        print 'paint'
        if self.selected():
            print 'paint selected'
            p.drawPixmap(3,0,self.highl)
        else:
            QListBoxPixmap.paint(p)
        
class StyleCombo(QComboBox):
    """ QComboBox for sets of sample pixmaps

    The StyleCombo allows selection from a set of pixmaps.  It
    provides a 'normal' and a 'highlighted' version of the pixmap.
    The pixmap's sizes are dynamically adjusted to the combobox size."""

    def __init__(self, parent=None, name='StyleCombo'):
        QComboBox.__init__(self, 0, parent, name)
        self.standardColors = [Qt.black, Qt.white, Qt.darkGray, \
                              Qt.gray, Qt.lightGray, Qt.red, \
                              Qt.green, Qt.blue, Qt.cyan, \
                              Qt.magenta, Qt.yellow, Qt.darkRed, \
                              Qt.darkGreen, Qt.darkBlue, Qt.darkCyan, \
                              Qt.darkMagenta, Qt.darkYellow]

        self.standardPenStyles = [Qt.PenStyle.NoPen, \
                                  Qt.PenStyle.SolidLine, \
                                  Qt.PenStyle.DashLine, \
                                  Qt.PenStyle.DotLine, \
                                  Qt.PenStyle.DashDotLine, \
                                  Qt.PenStyle.DashDotDotLine]

        self.standardBrushStyles = [Qt.BrushStyle.NoBrush, \
                                    Qt.BrushStyle.SolidPattern, \
                                    Qt.BrushStyle.Dense1Pattern, \
                                    Qt.BrushStyle.Dense2Pattern, \
                                    Qt.BrushStyle.Dense3Pattern, \
                                    Qt.BrushStyle.Dense4Pattern, \
                                    Qt.BrushStyle.Dense5Pattern, \
                                    Qt.BrushStyle.Dense6Pattern, \
                                    Qt.BrushStyle.Dense7Pattern, \
                                    Qt.BrushStyle.HorPattern, \
                                    Qt.BrushStyle.VerPattern, \
                                    Qt.BrushStyle.CrossPattern, \
                                    Qt.BrushStyle.BDiagPattern, \
                                    Qt.BrushStyle.FDiagPattern, \
                                    Qt.BrushStyle.DiagCrossPattern]
  

    def resizeEvent(self, resizeEvent):
        QComboBox.resizeEvent(self, resizeEvent)
        #self.drawAllPixmaps()

    def paintEvent(self, paintEvent):
        QComboBox.paintEvent(self, paintEvent)

        if (self.hasFocus() and self.style().inherits("QWindowsStyle")):
            if (not(self.listBox().text(currentItem()))):
                    p = QPainter(this)
                    nm = QPixmap()
                    hl = QPixmap()
                    self.drawPixmap(nm, hl, self.currentItem())
                    p.drawPixmap(4, (self.height() - hl.height())/2, hl)


    def enabledChange(self, oldEnabled):
        self.drawAllPixmaps()
        QComboBox.enabledChange(oldEnabled)
                 
    def paletteChange(self, oldPalette):
        self.drawAllPixmaps()
        QComboBox.paletteChange(oldPalette)

    def pixmapSize(self):
        #r = self.style().comboButtonRect(0, 0, self.width(), self.height())
        r = QRect(0,0,self.width(), self.height())
        return QSize(r.width()-4, r.height()-2)
        
    def drawAllPixmaps(self):
        lb = self.listBox()

        i = 0
        while (i < self.count()):
            if lb.text(i).isNull():
                nm = QPixmap()
                hl = QPixmap()
                self.drawPixmap(nm,hl,i)
                item = StyleComboItem(nm,hl)
                lb.changeItem(nm, i)
            i = i + 1


class PenStyleCombo(StyleCombo):
    """ ComboBox for selecting pen styles.

    The available pen styles are:
    NoPen - no outline is drawn
    SolidLine - solid line (default)
    DashLine - - - (dashes) line
    DotLine * * * (dots) line
    DashDotLine - * - * line
    DashDotDotLine - ** - ** line"""

    def __init__(self, parent=None, name='PenStyleCombo'):
        StyleCombo.__init__(self, parent, name)

        lb = self.listBox()
        lb.insertItem(self.tr('None'), 0)
        i = Qt.PenStyle.SolidLine
        while i <= Qt.PenStyle.DashDotDotLine:
            nm = QPixmap()
            hl = QPixmap()
            self.drawPixmap(nm,hl,i)
            item = StyleComboItem(nm,hl)
            lb.insertItem(nm, i)
            i = i + 1

        self.setCurrentItem(1)

    def setCurrentStyle(self, style):
        self.setCurrentItem(style)

    def currentStyle(self):
        return self.standardPenStyles[self.currentItem()]

    def drawPixmap(self, normal, highlighted, i):
        p = QPainter()

        normal.resize(self.pixmapSize())
        highlighted.resize(self.pixmapSize())

        normal.fill(Qt.white)
        p.begin(normal)
        p.setPen(self.standardPenStyles[i])
        p.drawLine(2, normal.height()/2, normal.width() - 4, normal.height()/2)
        p.end()
        

class BrushStyleCombo(StyleCombo):

    def __init__(self, parent=None, name='BrushStyleCombo'):
        StyleCombo.__init__(self, parent, name)

        lb = self.listBox()
        lb.insertItem(self.tr('Transparent'), 0)
        i = Qt.BrushStyle.SolidPattern
        while i <= Qt.BrushStyle.DiagCrossPattern:
            nm = QPixmap()
            hl = QPixmap()
            self.drawPixmap(nm,hl,i)
            item = StyleComboItem(nm,hl)
            lb.insertItem(nm, i)
            i = i + 1

        self.setCurrentItem(1)

    def setCurrentStyle(self, style):
        self.setCurrentItem(style)

    def drawPixmap(self, normal, highlighted, i):
        p = QPainter()

        normal.resize(self.pixmapSize())
        highlighted.resize(self.pixmapSize())

        normal.fill(Qt.white)
        p.begin(normal)
        p.fillRect(2,3,normal.width()-4, normal.height()-6, \
                   QBrush(Qt.black, self.standardBrushStyles[i]))
        p.end()


class ColorCombo(StyleCombo):
    """ ComboBox for selecting colors

    Allows selection from the 19 predefined QColor objects:
    black, white, darkGray, lightGray, red, green, blue, cyan,
    magenta, yellow, darkRed, darkGreen, darkBlue, darkCyan,
    darkMagenta, darkYellow, color0 and color1"""

    def __init__(self, parent=None, name='ColorCombo'):
        StyleCombo.__init__(self, parent, name)
        lb = self.listBox()
        for i in range(0,17):
            nm = QPixmap()
            hl = QPixmap()
            self.drawPixmap(nm, hl, i)
            item = StyleComboItem(nm, hl)
            lb.insertItem(nm, i)

    def setCurrentColor(self, color):
        for i in range(1,17):
            if color == self.standardColors[i]:
                self.setCurrentItem(i)

    def currentColor(self):
        i = self.currentItem()
        if i < 17:
            return self.standardColors[i]
        else:
            return QColor()

    def drawPixmap(self, normal, highlighted, index):
        p = QPainter()
        normal.resize(self.pixmapSize())
        normal.fill(Qt.white)
        
        if (index < 0) or (index > 17):
            c = Qt.white
        elif self.isEnabled():
            c = self.standardColors[index]
        else:
            c = Qt.red
            #c = self.colorGroup().text()

        p.begin(normal)
        p.fillRect(2,3,normal.width()-4, normal.height()-6, QBrush(c))
        #p.setPen(self.colorGroup().text())
        #p.setBrush(self.colorGroup().text())
        #p.drawRect(2,3,normal.width() - 4, normal.height()-6)
        p.end()

        """        highlighted = normal

        bm = QBitmap(self.pixmapSize(), 1)
        p.begin(bm)
        p.fillRect(2,3,normal.width()-4, normal.height() - 6, \
                   QBrush(Qt.color1))
        p.end()
        normal.setMask(bm)
        highlighted.setMask(bm)"""
        
class VectorStyleCombo(StyleCombo):

    def __init__(self, parent=None, name='VectorStyleCombo'):
        pass

    def drawPixmap(normal, highlighted, i):
        pass
    

