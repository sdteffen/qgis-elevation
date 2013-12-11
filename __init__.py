#! /usr/bin/env python
#
# This file is part of the QGIS Elevation Plugin
#
# __init__.py - load Elevation class from file Elevation.py
#
# Copyright 2010, 2013 Steffen Macke <sdteffen@sdteffen.de>
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
def name(): 
	return "Elevation" 
def description():
	return "Obtain and display point elevation data using Google Maps"
def version(): 
	return "Version 0.3.0" 
def qgisMinimumVersion():
	return "2.0"
def classFactory(iface): 
	# load Elevation class from file Elevation
	from Elevation import Elevation 
	return Elevation(iface)
