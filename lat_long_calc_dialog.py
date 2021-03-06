# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LatLongCalcDialog
                                 A QGIS plugin
 Allows coversion Long-Lat between decimal degrees and DMS
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-03-23
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Jiri Kalina
        email                : jiri.kalina.jr@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'lat_long_calc_dialog_base.ui'))


class LatLongCalcDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(LatLongCalcDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    # CONNECTING SIGNALS TO SLOTS:
    # ---- Click events for "latDMStoDD()" ----
        # Click event for "Lat. - Degrees" field
        self.spbLatD.valueChanged.connect(self.latDMStoDD)
        # Click event for "Lat. - Minutes" field
        self.spbLatM.valueChanged.connect(self.latDMStoDD)
        # Click event for "Lat. - Seconds" field
        self.spbLatS.valueChanged.connect(self.latDMStoDD)
        # Click event for "Lat - Hemmisphere" combo box
        self.cmbLatH.currentTextChanged.connect(self.latDMStoDD)

    # ---- Click events for "longDMStoDD()" ----
        # Click event for "Long. - Degrees" field
        self.spbLongD.valueChanged.connect(self.longDMStoDD)
        # Click event for "Long. - Minutes" field
        self.spbLongM.valueChanged.connect(self.longDMStoDD)
        # Click event for "Long. - Seconds" field
        self.spbLongS.valueChanged.connect(self.longDMStoDD)
        # Click event for "Long - Hemmisphere" combo box
        self.cmbLongH.currentTextChanged.connect(self.longDMStoDD)

    # ---- Click events for "latDDtoDMS()" & "longDDtoDMS()" ----
        # Signal goes from "spbLongDD" and we conncet to
        #self.spbLatDD.currentTextChanged.connect(self.latDDtoDMS)
        self.spbLatDD.editingFinished.connect(self.latDDtoDMS)
        self.spbLongDD.editingFinished.connect(self.longDDtoDMS)


    def latDMStoDD(self):
        iDeg = self.spbLatD.value()
        iMin = self.spbLatM.value()
        dSec = self.spbLatS.value()
        sHem = self.cmbLatH.currentText()

        dDD = float(iDeg) + iMin/60 + dSec/3600
        # Convert to negative coords. for Southern hemmisphere
        if sHem == 'S':
            dDD = dDD * -1
        self.spbLatDD.setValue(dDD)


    def longDMStoDD(self):
        iDeg = self.spbLongD.value()
        iMin = self.spbLongM.value()
        dSec = self.spbLongS.value()
        sHem = self.cmbLongH.currentText()

        dDD = float(iDeg) + iMin/60 + dSec/3600
        # Convert to negative coords. for West - East
        if sHem == 'W':
            dDD = dDD * -1

        self.spbLongDD.setValue(dDD)


    def latDDtoDMS(self):
        dDD = self.spbLatDD.value()

        iDeg = int(dDD)
        dMin = (dDD-iDeg)*60
        iMin = int(dMin)
        dSec = (dMin - iMin)*60

        self.spbLatD.setValue(abs(iDeg))
        self.spbLatM.setValue(abs(iMin))
        self.spbLatS.setValue(abs(dSec))

        if dDD < 0:
            self.cmbLatH.setCurrentText('S')
        else:
            self.cmbLatH.setCurrentText('N')


    def longDDtoDMS(self):
        dDD = self.spbLongDD.value()

        iDeg = int(dDD)
        dMin = (dDD-iDeg)*60
        iMin = int(dMin)
        dSec = (dMin - iMin)*60

        self.spbLongD.setValue(abs(iDeg))
        self.spbLongM.setValue(abs(iMin))
        self.spbLongS.setValue(abs(dSec))

        if dDD < 0:
            self.cmbLongH.setCurrentText('W')
        else:
            self.cmbLongH.setCurrentText('E')
