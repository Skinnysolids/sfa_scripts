import logging

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QFileDialog
from shiboken2 import wrapInstance
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pnc
from pymel.core.system import Path


log = logging.getLogger(__name__)


def maya_main_window():
    """return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """ScatterTool UI Class"""
    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.scat = Scatter()
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
        self.select_note = self._create_select_note()
        self.button_lay = self._create_button_ui()
        self.objchoose = self._create_obj_choose()
        self.randomscale = self._create_random_scale()
        self.randomrotation = self._create_random_rotation()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.select_note)
        self.main_lay.addLayout(self.objchoose)
        self.main_lay.addLayout(self.randomscale)
        self.main_lay.addLayout(self.randomrotation)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_select_note(self):
        self.note = QtWidgets.QLabel("Note: When multiple objects are "
                                     "selected, the Select buttons "
                                     "will only choose the first object "
                                     "in that selection.")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.note)
        return layout

    def _create_random_rotation(self):
        """creates a random rotation editable text box"""
        self.random_rot_max_label = QtWidgets.QLabel("Random Rotation Max")
        self.rand_rot_max = QtWidgets.QLineEdit("180")
        self.random_rot_min_label = QtWidgets.QLabel("Random Rotation Min")
        self.rand_rot_min = QtWidgets.QLineEdit("0")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_rot_max_label)
        layout.addWidget(self.rand_rot_max)
        layout.addWidget(self.random_rot_min_label)
        layout.addWidget(self.rand_rot_min)
        return layout

    def _create_random_scale(self):
        """creates a random scale editable text box"""
        self.random_scale_max_label = QtWidgets.QLabel("Random Scale Max ")
        self.random_scale_min_Label = QtWidgets.QLabel("Random Scale Min")
        self.rand_scale_max = QtWidgets.QLineEdit("2")
        self.rand_scale_min = QtWidgets.QLineEdit(".5")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_scale_max_label)
        layout.addWidget(self.rand_scale_max)
        layout.addWidget(self.random_scale_min_Label)
        layout.addWidget(self.rand_scale_min)
        return layout

    def _create_obj_choose(self):
        """This creates two combobox select menus for selecting recipient
        and obj to scatter"""
        self.to_scatter_label = QtWidgets.QLabel("Obj to Scatter:")
        self.scatter_on_label = QtWidgets.QLabel("Obj to Scatter On:")
        self.to_scatter_line_edit = QtWidgets.QLineEdit()
        self.to_scatter_btn = QtWidgets.QPushButton("Select Object")
        self.scatter_on_line_edit = QtWidgets.QLineEdit()
        self.scatter_on_object_button = QtWidgets.QPushButton("Select Object")
        self.scatter_on_verts_button = QtWidgets.QPushButton("Select Vertices")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.to_scatter_label)
        layout.addWidget(self.to_scatter_line_edit)
        layout.addWidget(self.to_scatter_btn)
        layout.addWidget(self.scatter_on_label)
        layout.addWidget(self.scatter_on_line_edit)
        layout.addWidget(self.scatter_on_object_button)
        layout.addWidget(self.scatter_on_verts_button)
        return layout

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        layout.addWidget(self.cancel_btn)
        return layout

    def create_connections(self):
        """TO DO: CONNECT THE BUTTONS"""
        self.cancel_btn.clicked.connect(self.cancel)

        self.to_scatter_btn.clicked.connect(self.select_scatter)

        self.scatter_on_object_button.clicked.connect\
            (self.select_to_scatter_obj)
        self.scatter_on_verts_button.clicked.connect\
            (self.select_to_scatter_verts)
        self.scatter_btn.clicked.connect(self.scatter)

    @QtCore.Slot()
    def scatter(self):
        pass

    @QtCore.Slot()
    def select_to_scatter_obj(self):
        #TODO create error thingie if user selected verts and then pressed
        #this button
        self.scatter_on_line_edit.setText(
            self.scat.select_an_object_to_scatter_to())

    @QtCore.Slot()
    def select_to_scatter_verts(self):
        # TODO create error thingie if user selected objs and then pressed
        # this button
        self.scatter_on_line_edit.setText(
            self.scat.select_verts_to_scatter_to())

    @QtCore.Slot()
    def select_scatter(self):
        self.to_scatter_line_edit.setText(self.scat.select_obj_to_scatter())

    @QtCore.Slot()
    def cancel(self):
        """quits the dialogue"""
        self.close()

class Scatter(object):
    def __init__(self):
        self.obj_to_scatter = ''
        self.obj_to_scatter_on = ''
        self.verts_to_scatter_on = ''
        self.scale_max = 2
        self.scale_min = 0.5
        self.rot_max = 180
        self.rot_min = 0

    def Scatter(self):
        pass

    def random_scale_instance(self):
        pass

    def random_rotate_instance(self):
        pass

    def select_an_object_to_scatter_to(self):
        self.selected_objs = cmds.ls(sl=True)
        self.obj_to_scatter = self.selected_objs[0]
        self.verts_to_scatter_on = cmds.polyListComponentConversion(
            self.obj_to_scatter, toVertex=True)
        return str(self.verts_to_scatter_on)


    def select_verts_to_scatter_to(self):
        self.verts_to_scatter_on = cmds.ls(sl=True, flatten=True)
        return str(self.verts_to_scatter_on)

    def select_obj_to_scatter(self):
        self.selected_objs = cmds.ls(sl=True)
        self.obj_to_scatter_on = self.selected_objs[0]
        return str(self.obj_to_scatter_on)
