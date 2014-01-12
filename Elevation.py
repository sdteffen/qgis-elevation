#
# This file is part of the QGIS Elevation Plugin
#
# Elevation.py - load Elevation class from file Elevation.py
#
# Copyright 2010, 2013, 2014 Steffen Macke <sdteffen@sdteffen.de>
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
# The QGIS Python bindings are required to run this file
# 
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *

import sys, os, httplib, json, tempfile, urllib

# GeoCoding Utils
from Utils import *
# Elevation imports
from resources import *
from numericmarkers import *
from ImageDialog import *

class Elevation: 

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		self.canvas = iface.mapCanvas()
		# store layer id
		self.layerid = ''			
	
	def initGui(self):  
		self.obtainAction = QAction(QIcon(":/plugins/elevation/elevation_icon.png"), QCoreApplication.translate('Elevation', "&Obtain Elevation"), self.iface.mainWindow())       
		self.aboutAction = QAction(QIcon(":/plugins/elevation/about_icon.png"), QCoreApplication.translate('Elevation', "&About"), self.iface.mainWindow())    
		self.iface.addPluginToMenu("Elevation", self.obtainAction)
		self.iface.addPluginToMenu("Elevation", self.aboutAction)
		self.iface.addToolBarIcon(self.obtainAction)

		QObject.connect(self.obtainAction, SIGNAL("triggered()"), self.obtain) 
		QObject.connect(self.aboutAction, SIGNAL("triggered()"), self.about) 
	
	def unload(self):
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu("Elevation", self.obtainAction)
		self.iface.removePluginMenu("Elevation", self.aboutAction)
		self.iface.removeToolBarIcon(self.obtainAction)
	
	def about(self):
		infoString = QCoreApplication.translate('Elevation', "QGIS Elevation Plugin 0.4.0<br />This plugin allows to mark point elevations in Google Maps.<br />Copyright (c) 2010, 2013 Steffen Macke<br /><a href=\"http://polylinie.de/elevation\">polylinie.de/elevation</a><br/>You have to accept the<br/><a href=\"http://code.google.com/intl/en/apis/maps/terms.html\">Google Maps APIs Terms of Service</a>\n")
		QMessageBox.information(self.iface.mainWindow(), "About Elevation", infoString)
	
	# Obtain elevation
	def obtain(self):
		chk = self.check_settings()
		if len(chk) :
			QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('Elevation', "Elevation plugin error"), chk)   
			return                    
		sb = self.iface.mainWindow().statusBar()
		sb.showMessage(QCoreApplication.translate('Elevation', "Click on the map to obtain the elevation"))
		ct = ClickTool(self.iface,  self.obtain_action);
		self.iface.mapCanvas().setMapTool(ct)

	def obtain_action(self, point) :
		epsg4326 = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
		self.reprojectgeographic = QgsCoordinateTransform(self.iface.mapCanvas().mapRenderer().destinationCrs(), epsg4326)
		pt = self.reprojectgeographic.transform(point)
		conn = httplib.HTTPConnection("maps.googleapis.com")
		QgsMessageLog.instance().logMessage( "http://maps.googleapis.com/maps/api/elevation/json?locations=" + str(pt[1])+","+str(pt[0])+"&sensor=false", "Elevation")
		conn.request("GET", "/maps/api/elevation/json?locations=" + str(pt[1])+","+str(pt[0])+"&sensor=false")
		response = conn.getresponse()				
		jsonresult = response.read()
		try:
			results = json.loads(jsonresult).get('results')
			if 0 < len(results):
				elevation = int(round(results[0].get('elevation')))
				# save point
				self.save_point(point, elevation)
				#find marker
				marker = 'http://bit.ly/aUwrKs'
				for x in range(0, 1000):
					if numericmarkers.has_key(elevation+x) :
						marker = numericmarkers.get(elevation+x)
						break
					if numericmarkers.has_key(elevation-x):
						marker = numericmarkers.get(elevation-x)
						break
				# create map
				image = tempfile.mkstemp(suffix='png')
				os.close(image[0])
				urllib.urlretrieve('http://maps.google.com/maps/api/staticmap?size=640x480&maptype=terrain\&markers=icon:'+marker+'|'+str(pt[1])+','+str(pt[0])+'&mobile=true&sensor=false', image[1])
				QgsMessageLog.instance().logMessage('http://maps.google.com/maps/api/staticmap?size=640x4802&maptype=terrain\&markers=icon:'+marker+'|'+str(pt[1])+','+str(pt[0])+'&mobile=true&sensor=false')
				dlg = ImageDialog()
				dlg.image.setPixmap(QPixmap(image[1]))
				dlg.show()
				dlg.exec_()
				if os.path.exists(image[1]):
					os.unlink(image[1])
			else:
				QMessageBox.warning(self.iface.mainWindow(), 'Elevation', 'HTTP GET Request failed.', QMessageBox.Ok, QMessageBox.Ok)
		except ValueError, e:
			QMessageBox.warning(self.iface.mainWindow(), 'Elevation', 'JSON decode failed: '+str(jsonresult), QMessageBox.Ok, QMessageBox.Ok)
 
	# save point to file, point is in project's crs
	def save_point(self, point, elevation):
		# create and add the point layer if not exists or not set
		if not QgsMapLayerRegistry.instance().mapLayer(self.layerid) :
			# create layer with same CRS as project
			self.layer = QgsVectorLayer("Point?crs=epsg:4326", "Elevation Plugin Results", "memory")
			self.provider = self.layer.dataProvider()

			# add fields
			self.provider.addAttributes( [QgsField("elevation", QVariant.Double)] )
			self.layer.updateFields()

			# Labels on
			label = self.layer.label()
			label.setLabelField(QgsLabel.Text, 0) 
			self.layer.enableLabels(True)

			# add layer if not already
			QgsMapLayerRegistry.instance().addMapLayer(self.layer)

			# store layer id
			self.layerid = QgsMapLayerRegistry.instance().mapLayers().keys()[-1]

		# add a feature
		fet = QgsFeature()
		fet.initAttributes(1)
		fet.setGeometry(QgsGeometry.fromPoint(self.reprojectgeographic.transform(point)))
		fet.setAttribute(0, elevation)
		self.provider.addFeatures( [ fet ] )

		# update layer's extent when new features have been added
		# because change of extent in provider is not propagated to the layer
		self.layer.updateExtents()

		self.canvas.refresh()

	# check project settings before obtaining elevations
	# return an error string
	def check_settings (self) :
		p = QgsProject.instance()
		error = ''
		proj4string = self.iface.mapCanvas().mapRenderer().destinationCrs().toProj4()
		return error

if __name__ == "__main__":
	pass
    
