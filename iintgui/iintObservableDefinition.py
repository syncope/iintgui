# Copyright (C) 2017-9  Christoph Rosemann, DESY, Notkestr. 85, D-22607 Hamburg
# email contact: christoph.rosemann@desy.de
#
# iintgui is an application for the ADAPT framework
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation in  version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.

from PyQt4 import QtCore, QtGui, uic
from . import getUIFile


class iintObservableDefinition(QtGui.QWidget):
    motorName = QtCore.pyqtSignal(str)
    observableDicts = QtCore.pyqtSignal(dict, dict)
    doDespike = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(iintObservableDefinition, self).__init__(parent)
        self.setWindowTitle("Observable definition")
        uic.loadUi(getUIFile.getUIFile("iintobservable.ui"), self)
        self._obsDict = {}
        self._despikeDict = {}
        self._trapintDict = {}
        self.motorCB.currentIndexChanged.connect(self.setMotor)
        self.observableDetectorCB.currentIndexChanged.connect(self.setObservable)
        self.observableMonitorCB.currentIndexChanged.connect(self.setMonitor)
        self.observableTimeCB.currentIndexChanged.connect(self.setTime)
        self._useAttenuationFactor = False
        self.observableAttFaccheck.stateChanged.connect(self.toggleAttFac)
        self.observableAttFacCB.currentIndexChanged.connect(self.setAttFac)
        self.observableAttFacCB.setDisabled(True)
        self.despikeCheckBox.stateChanged.connect(self.toggleDespiking)
        self._despike = False
        self._notEnabled(True)
        self.obsDisplayBtn.clicked.connect(self.emittit)
        self.obsDisplayBtn.clicked.connect(self.activateShowScanProfile)
        #~ self.obsDisplayBtn.clicked.connect(self.activateMCA)
        self._observableName = 'observable'
        self.motorCB.setToolTip("Choose the independent axis of the scan display (the 'motor'), e.g. from the scan command.")
        self.label.setToolTip("The shorthand notation for the used formula to calculate\nthe number of counts at the given motor position.")
        self.observableDetectorCB.setToolTip("Chose the detector entry from the scan file information.")
        self.observableMonitorCB.setToolTip("Chose the monitor name from the scan file information.")
        self.observableTimeCB.setToolTip("Chose the time entry from the scan file information.")
        self.observableAttFaccheck.setToolTip("Chose the entry from the scan file information for an attenuation factor.")
        self.observableAttFacCB.setToolTip("Check the box to enable the choice of an attenuation factor entry.")
        self.despikeCheckBox.setToolTip("Check the box to run a despiking/filtering algorithm\non the scan data to dampen spikes/noise fluctuation.")
        self.overlayBtn.setToolTip("Open an overlay plot window to select scans to view at the same time.")
        self.obsDisplayBtn.setToolTip("Once everything is set, click this button to perform\nthe calculation of the observable data and open a display.")
        self.showScanProfile.setToolTip("Creates a stack of all scans as matrix, creating an image.\nThe result is stored in a file, which is shown in an external viewer.")
        self.trackData.setToolTip("Open a dialog to select column and header\ndata to be included in the output file.")
        self.maptracks.setToolTip("After tracked data has been selected, choose data to map.")
        #~ self.showMCA.hide()
        #~ self.showMCA.setDisabled(False)

    def _defaultSettings(self):
        self._obsDict = {}
        self._despikeDict = {}
        self._trapintDict = {}
        self._useAttenuationFactor = False
        self.observableAttFacCB.setDisabled(True)
        self.despikeCheckBox.setChecked(False)
        self._despike = False
        self._notEnabled(True)
        self._observableName = 'observable'
        self.deactivateShowScanProfile()
        #~ self.showMCA.setDisabled(False)
        self.trackData.setDisabled(True)

    def reset(self):
        self._defaultSettings()

    def activate(self):
        self._notEnabled(False)

    def activateMapTrack(self):
        self.maptracks.setDisabled(False)

    def deactivateMapTrack(self):
        self.maptracks.setDisabled(True)

    #~ def activateMCA(self):
        #~ self.showMCA.show()
        #~ self.showMCA.setDisabled(False)

    def passInfo(self, dataobject):
        if dataobject is None:
            self._notEnabled(True)
            return
        else:
            self._notEnabled(False)

        self._currentdataLabels = dataobject.getLabels()
        self.scantype.setText(dataobject.getScanType())
        self.scantype.setStyleSheet("color: red;")
        #~ self.observableMotorLabel.setStyleSheet("color: blue;")
        self._scanmotorname = dataobject.getMotorName()

        # now set the texts and labels
        self.motorCB.clear()
        self.observableDetectorCB.clear()
        self.observableMonitorCB.clear()
        self.observableTimeCB.clear()
        self.observableAttFacCB.clear()
        self.motorCB.addItems(self._currentdataLabels)
        self.observableDetectorCB.addItems(self._currentdataLabels)
        self.observableMonitorCB.addItems(self._currentdataLabels)
        self.observableTimeCB.addItems(self._currentdataLabels)
        self.observableAttFacCB.addItems(self._currentdataLabels)
        if not self._useAttenuationFactor:
            self.observableAttFacCB.setDisabled(True)
            self._useAttenuationFactor = False
            self.observableAttFaccheck.setChecked(False)

    def _notEnabled(self, state):
        self.motorCB.setDisabled(state)
        self.observableDetectorCB.setDisabled(state)
        self.observableMonitorCB.setDisabled(state)
        self.observableTimeCB.setDisabled(state)
        self.observableAttFaccheck.setDisabled(state)
        self.observableAttFacCB.setDisabled(state)
        self.despikeCheckBox.setDisabled(state)
        self.overlayBtn.setDisabled(state)
        self.obsDisplayBtn.setDisabled(state)
        self.trackData.setDisabled(state)

    def activateShowScanProfile(self):
        self.showScanProfile.setDisabled(False)

    def deactivateShowScanProfile(self):
        self.showScanProfile.setDisabled(True)

    def toggleAttFac(self):
        # creates trouble at reset 
        self.observableAttFacCB.setDisabled(self._useAttenuationFactor)
        self._useAttenuationFactor = not self._useAttenuationFactor

    def setMotor(self, motorindex):
        self._motorname = self._currentdataLabels[motorindex]
        self.motorName.emit(self._motorname)

    def setObservable(self, obsindex):
        self._detname = self._currentdataLabels[obsindex]

    def setMonitor(self, monindex):
        self._monname = self._currentdataLabels[monindex]

    def setTime(self, timeindex):
        self._timename = self._currentdataLabels[timeindex]

    def setAttFac(self, attfacindex):
        # need to sort out the pre-condition
        #~ if(self._useAttenuationFactor):
        self._attenfname = self._currentdataLabels[attfacindex]

    def toggleDespiking(self):
        self._despike = not self._despike
        #~ self.doDespike.emit(self._despike)

    def emittit(self):
        self._obsDict["type"] = "iintdefinition"
        self._obsDict["input"] = "rawdata"
        self._obsDict["motor_column"] = self._motorname
        self._obsDict["detector_column"] = self._detname
        self._obsDict["monitor_column"] = self._monname
        self._obsDict["exposureTime_column"] = self._timename
        self._obsDict["output"] = self._observableName
        self._obsDict["id"] = "scannumber"
        if(self._useAttenuationFactor):
            self._obsDict["attenuationFactor_column"] = self._attenfname
        else:
            try:
                del self._obsDict["attenuationFactor_column"]
            except KeyError:
                # maybe it doesn't exist yet
                pass

        if(self._despike):
            self._despikeDict["type"] = "filter1d"
            self._despikeDict["method"] = "p09despiking"
            self._despikeDict["input"] = "observable"
            self._despikeDict["output"] = "despikedObservable"
        else:
            self._despikeDict = {}
        self._trapintDict["type"] = "trapezoidintegration"
        self._trapintDict["motor"] = self._motorname
        self._trapintDict["observable"] = "signalObservable"
        self._trapintDict["output"] = "trapezoidIntegral"

        self.observableDicts.emit(self._obsDict, self._despikeDict)

    def setParameterDicts(self, obsDict, despDict):
        index = self.motorCB.findText(obsDict["motor_column"], QtCore.Qt.MatchExactly)
        print("setting: find the motor, index is: " +str(index))
        print(" the dict says: " + str(obsDict["motor_column"]))
        if index >= 0:
            self.motorCB.setCurrentIndex(index)

        # first get index of element
        index = self.observableDetectorCB.findText(obsDict["detector_column"], QtCore.Qt.MatchExactly)
        if index >= 0:
            self.observableDetectorCB.setCurrentIndex(index)

        index = self.observableMonitorCB.findText(obsDict["monitor_column"], QtCore.Qt.MatchExactly)
        if index >= 0:
            self.observableMonitorCB.setCurrentIndex(index)

        index = self.observableTimeCB.findText(obsDict["exposureTime_column"], QtCore.Qt.MatchExactly)
        if index >= 0:
            self.observableTimeCB.setCurrentIndex(index)

        try:
            index = self.observableAttFacCB.findText(obsDict["attenuationFactor_column"], QtCore.Qt.MatchExactly)
            if index >= 0:
                self.observableAttFacCB.setCurrentIndex(index)
                self.observableAttFaccheck.setChecked(True)
                self.observableAttFacCB.setDisabled(False)
        except KeyError:
            # there is no attenuation factor column
            self._useAttenuationFactor = False
            self.observableAttFacCB.setDisabled(True)
            pass

        if (despDict != {}):
            self.despikeCheckBox.setChecked(True)
