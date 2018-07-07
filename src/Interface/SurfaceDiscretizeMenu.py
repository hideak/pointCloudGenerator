"""
# Module: SurfaceDiscretizeMenu.py
# Description: This module contains the Surface Discretization Side Widget Menu UI
for calling the discretization functions.
# Author: Willian Hideak Arita da Silva.
"""

# System Imports:
import sys

# PyQt5 Imports:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QToolButton, QMessageBox, QLineEdit, \
                            QCheckBox, QRadioButton, QSlider

# Local Imports:
from Import.IGESImport import *
from Actions.Functions import *
from Discretization.DiscretizeModel import *
from Resources.Strings import MyStrings

class surfaceDiscretizeMenu(QWidget):
    """
    # Class: surfaceDiscretizeMenu.
    # Description: This class provides a side menu with some options to configure
    the Surface Discretization process.
    """

    def __init__(self, parent):
        """
        # Method: __init__.
        # Description: The init method for initializing the inhirited properties.
        # Parameters: * MainWindow parent = A reference for the main window object.
        """

        super().__init__()
        self.initUI(parent)

    def initUI(self, parent):
        """
        # Method: initUI.
        # Description: This method initializes the User Interface Elements of the
        Surface Discretize Menu side widget.
        # Parameters: * MainWindow parent = A reference for the main window object.
        """

        grid = QGridLayout()
        self.setLayout(grid)

        label1 = QLabel(MyStrings.surfaceDiscretizeDescription, self)
        grid.addWidget(label1, 0, 0, 1, 2)

        label2 = QLabel(MyStrings.selectionModeHeader, self)
        grid.addWidget(label2, 1, 0, 1, 2)

        label3 = QLabel(MyStrings.askingForSelectionMethod)
        grid.addWidget(label3, 2, 0, 1, 2)

        btn1 = QToolButton()
        btn1.setText(MyStrings.selectionModeSolids)
        btn1.clicked.connect(lambda: self.selectSolids(parent))
        btn1.setMinimumHeight(50)
        btn1.setMinimumWidth(130)
        btn1.setEnabled(False)
        grid.addWidget(btn1, 3, 0)

        btn2 = QToolButton()
        btn2.setText(MyStrings.selectionModeSurfaces)
        btn2.clicked.connect(lambda: self.selectSurfaces(parent))
        btn2.setMinimumHeight(50)
        btn2.setMinimumWidth(130)
        grid.addWidget(btn2, 3, 1)

        label4 = QLabel(MyStrings.entitySelectionHeader)
        grid.addWidget(label4, 4, 0, 1, 2)

        label5 = QLabel(MyStrings.askingForEntity, self)
        grid.addWidget(label5, 5, 0, 1, 2)

        self.selectedObject = QLineEdit()
        self.selectedObject.setReadOnly(True)
        self.selectedObject.setPlaceholderText(MyStrings.entityPlaceholder)
        grid.addWidget(self.selectedObject, 6, 0, 1, 2)

        btn3 = QToolButton()
        btn3.setText(MyStrings.addEntityOption)
        btn3.clicked.connect(lambda: self.addSelection(parent))
        btn3.setMinimumHeight(30)
        btn3.setMinimumWidth(266)
        grid.addWidget(btn3, 7, 0, 1, 2)

        label6 = QLabel(MyStrings.nonFlatDiscretizationHeader, self)
        grid.addWidget(label6, 8, 0, 1, 2)

        label7 = QLabel(MyStrings.askingForUParameter, self)
        grid.addWidget(label7, 9, 0, 1, 2)

        self.UParameter = QLineEdit()
        grid.addWidget(self.UParameter, 10, 0, 1, 2)

        label8 = QLabel(MyStrings.askingForVParameter, self)
        grid.addWidget(label8, 11, 0, 1, 2)

        self.VParameter = QLineEdit()
        grid.addWidget(self.VParameter, 12, 0, 1, 2)

        btn4 = QToolButton()
        btn4.setText(MyStrings.surfaceDiscretizeApply)
        btn4.clicked.connect(lambda: self.surfaceDiscretize(parent))
        btn4.setMinimumHeight(30)
        btn4.setMinimumWidth(266)
        grid.addWidget(btn4, 13, 0, 1, 2)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(14, 1)

    def surfaceDiscretize(self, parent):
        """
        # Method: surfaceDiscretize.
        # Description: Performs the discretization of a selected surface in the loaded CAD Model.
        # Parameters: * MainWindow parent = A reference for the main window object.
        """

        # Check if there is a point cloud present:
        if(parent.pointCloudObject):
            cleanCloud(parent)

        # Gets all the required parameters from the User Interface:
        Uparam = float(self.UParameter.displayText())
        Vparam = float(self.VParameter.displayText())

        # Loads the loading window:
        parent.loadingWindow.show()

        # Performs the surfaceDiscretization using the Discretization package:
        sequence = parent.selectedSequenceNumber
        points, normals = discretizeSurface(parent.entitiesObject[pos(sequence)], parent.entitiesObject,
                                            Uparam, Vparam)
        parent.faceSequenceNumbers.append(sequence)
        parent.faceNormalVectors.append(normals)
        parent.cloudPointsList.append(points)

        # Builds the generated point cloud:
        buildCloud(parent)

        # Updates some properties from the main window:
        parent.activeCloudFile = MyStrings.currentSessionGeneratedPoints

        # Closes the loading window:
        parent.loadingWindow.close()

    def selectSolids(self, parent):
        """
        # Method: selectSolids.
        # Description: Method for activating the Neutral Selection Mode in PythonOCC lib.
        The Neutral Selection Mode allows the selection of whole solid CAD models.
        # Parameters: * MainWindow parent = A reference for the main window object.
        """
        parent.canvas._display.SetSelectionModeNeutral()
        if(parent.pointCloudObject):
            restoreCloud(parent)

    def selectSurfaces(self, parent):
        """
        # Method: selectSurfaces.
        # Description: Method for activating the Face Selection Mode in the PythonOCC lib.
        The Face Selection Mode allows the selection of each separated face of the CAD model.
        # Parameters: * MainWindow parent = A reference for the main window object.
        """
        parent.canvas._display.SetSelectionModeFace()
        if(parent.pointCloudObject):
            restoreCloud(parent)

    def addSelection(self, parent):
        """
        # Method: addSelection.
        # Description: Method for adding the current selected shape in the selectedObject
        parameter of the main window. The current selected shape is retrieved by a specific
        function of the PythonOCC lib and is used for comparing with a list of loaded shapes
        of the CAD Model. With this association, it is possible to check the Sequence Number
        associated in the IGES file.
        # Parameters: * MainWindow parent = A reference for the main window object.
        """

        if parent.canvas._display.GetSelectedShapes():
            parent.shapeParameter1 = parent.canvas._display.GetSelectedShapes()[-1]
        else:
            return
        i = 0
        while i < len(parent.shapeList):
            if(parent.shapeParameter1.IsPartner(parent.shapeList[i])):
                break
            i += 1
        self.selectedObject.setText(parent.entitiesList[i][0])
        parent.selectedShape = parent.shapeList[i]
        parent.selectedSequenceNumber = 2*i + 1
