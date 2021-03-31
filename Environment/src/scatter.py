import logging

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QFileDialog
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pnc
from pymel.core.system import Path


log = logging.getLogger(__name__)


def maya_main_window():
    """return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class ScatterTool(QtWidgets.QDialog):
    """SmartSave UI Class"""
    def __init__(self):
        super(ScatterTool, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        # Note: Need to code connections
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 28px")
        self.button_lay = self._create_button_ui()
        self.objchoose = self._create_obj_choose()
        self.randomscale = self._create_random_scale()
        self.randomrotation = self._create_random_rotation()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.objchoose)
        self.main_lay.addLayout(self.randomscale)
        self.main_lay.addLayout(self.randomrotation)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_random_rotation(self):
        """creates a random rotation editable text box"""
        self.random_rot_label = QtWidgets.QLabel("Random Rotation "
                                                   "(numbers only please) :")
        self.rand_rot = QtWidgets.QLineEdit("1")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_rot_label)
        layout.addWidget(self.rand_rot)
        return layout

    def _create_random_scale(self):
        """creates a random scale editable text box"""
        self.random_scale_label = QtWidgets.QLabel("Random Scale "
                                                   "(numbers only please) :")
        self.rand_scale = QtWidgets.QLineEdit("1")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_scale_label)
        layout.addWidget(self.rand_scale)
        return layout

    def _create_obj_choose(self):
        """This creates two combobox select menus for selecting recipient
        and obj to scatter"""
        self.to_scatter_label = QtWidgets.QLabel("Obj to Scatter:")
        self.scatter_on_label = QtWidgets.QLabel("Obj to Scatter On:")
        self.to_scatter = QtWidgets.QLineEdit()
        self.to_scatter_button = QtWidgets.QPushButton("Select")
        self.scatter_on = QtWidgets.QLineEdit()
        self.scatter_on_button = QtWidgets.QPushButton("Select")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.to_scatter_label)
        layout.addWidget(self.to_scatter)
        layout.addWidget(self.to_scatter_button)
        layout.addWidget(self.scatter_on_label)
        layout.addWidget(self.scatter_on)
        layout.addWidget(self.scatter_on_button)
        return layout

    def _create_button_ui(self):
        self.save_btn = QtWidgets.QPushButton("Scatter")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.save_btn)
        layout.addWidget(self.cancel_btn)
        return layout


    def create_connections(self):
        """TO DO: CONNECT THE BUTTONS"""
        pass