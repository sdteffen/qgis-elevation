#
# This file is part of the QGIS Elevation Plugin
#
# ImageDialog.py - Display a simple dialog with an image  
#
# Copyright 2014 Steffen Macke <sdteffen@sdteffen.de>
#
# The QGIS Elevation plugin is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2, or (at your option) any later version.
#
# The QGIS Elevation plugin is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with program; see the file COPYING. If not,
# write to the Free Software Foundation, Inc., 59 Temple Place
# - Suite 330, Boston, MA 02111-1307, USA.
#

from PyQt4 import QtCore, QtGui

class ImageDialog(QtGui.QDialog):
	def setupUi(self):
		self.setObjectName('Elevation')
		self.resize(640,480)
		self.image = QtGui.QLabel(self)
		self.image.setGeometry(0,0,640,480)

	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.setupUi()

