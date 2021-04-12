import logging

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QFileDialog
from shiboken2 import wrapInstance
import maya.OpenMaya as oM
import maya.OpenMayaUI as omUI
import maya.cmds as cmds
import pymel.core as pnc
from pymel.core.system import Path
import random as rand

log = logging.getLogger(__name__)


def maya_main_window():
    """return the maya main window widget"""
    main_window = omUI.MQtUtil.mainWindow()
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
        self.randomscalemax = self._create_random_scale_max()
        self.randomscalemin = self._create_random_scale_min()
        self.randomrotationmax = self._create_random_rotation_max()
        self.randomrotationmin = self._create_random_rotation_min()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.select_note)
        self.main_lay.addLayout(self.objchoose)
        self.main_lay.addLayout(self.randomscalemax)
        self.main_lay.addLayout(self.randomscalemin)
        self.main_lay.addLayout(self.randomrotationmax)
        self.main_lay.addLayout(self.randomrotationmin)
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

    def _create_random_rotation_max(self):
        """creates a random rotation editable text box"""
        self.random_rot_max_label_x = QtWidgets.QLabel("Random Rotation Max")
        self.random_rot_max_label_y = QtWidgets.QLabel("Random Rotation Max")
        self.random_rot_max_label_z = QtWidgets.QLabel("Random Rotation Max")
        self.rand_rot_max_x = QtWidgets.QLineEdit("180")
        self.rand_rot_max_y = QtWidgets.QLineEdit("180")
        self.rand_rot_max_z = QtWidgets.QLineEdit("180")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_rot_max_label_x)
        layout.addWidget(self.rand_rot_max_x)
        layout.addWidget(self.random_rot_max_label_y)
        layout.addWidget(self.rand_rot_max_y)
        layout.addWidget(self.random_rot_max_label_z)
        layout.addWidget(self.rand_rot_max_z)
        return layout

    def _create_random_rotation_min(self):
        self.random_rot_min_label_x = QtWidgets.QLabel("Random Rotation Min X")
        self.random_rot_min_label_y = QtWidgets.QLabel("Random Rotation Min Y")
        self.random_rot_min_label_z = QtWidgets.QLabel("Random Rotation Min Z")
        self.rand_rot_min_x = QtWidgets.QLineEdit("0")
        self.rand_rot_min_y = QtWidgets.QLineEdit("0")
        self.rand_rot_min_z = QtWidgets.QLineEdit("0")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_rot_min_label_x)
        layout.addWidget(self.rand_rot_min_x)
        layout.addWidget(self.random_rot_min_label_y)
        layout.addWidget(self.rand_rot_min_y)
        layout.addWidget(self.random_rot_min_label_z)
        layout.addWidget(self.rand_rot_min_z)
        return layout

    def _create_random_scale_max(self):
        """creates a random scale editable text box"""
        self.random_scale_max_label_x = QtWidgets.QLabel("Random Scale Max X")
        self.random_scale_max_label_y = QtWidgets.QLabel("Random Scale Max Y")
        self.random_scale_max_label_z = QtWidgets.QLabel("Random Scale Max Z")
        self.rand_scale_max_x = QtWidgets.QLineEdit("2")
        self.rand_scale_max_y = QtWidgets.QLineEdit("2")
        self.rand_scale_max_z = QtWidgets.QLineEdit("2")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_scale_max_label_x)
        layout.addWidget(self.rand_scale_max_x)
        layout.addWidget(self.random_scale_max_label_y)
        layout.addWidget(self.rand_scale_max_y)
        layout.addWidget(self.random_scale_max_label_z)
        layout.addWidget(self.rand_scale_max_z)
        return layout

    def _create_random_scale_min(self):
        self.random_scale_min_Label_x = QtWidgets.QLabel("Random Scale Min X")
        self.random_scale_min_Label_y = QtWidgets.QLabel("Random Scale Min Y")
        self.random_scale_min_Label_z = QtWidgets.QLabel("Random Scale Min Z")
        self.rand_scale_min_x = QtWidgets.QLineEdit(".5")
        self.rand_scale_min_y = QtWidgets.QLineEdit(".5")
        self.rand_scale_min_z = QtWidgets.QLineEdit(".5")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_scale_min_Label_x)
        layout.addWidget(self.rand_scale_min_x)
        layout.addWidget(self.random_scale_min_Label_y)
        layout.addWidget(self.rand_scale_min_y)
        layout.addWidget(self.random_scale_min_Label_z)
        layout.addWidget(self.rand_scale_min_z)
        return layout


    def _create_obj_choose(self):
        """This creates two combobox select menus for selecting recipient
        and obj to scatter"""
        self.to_scatter_label = QtWidgets.QLabel("Obj to Scatter:")
        self.scatter_on_label = QtWidgets.QLabel("Obj/Vertices to Scatter On:")
        self.to_scatter_line_edit = QtWidgets.QLineEdit()
        self.obj_to_scatter_btn = QtWidgets.QPushButton("Select Object")
        self.scatter_on_line_edit = QtWidgets.QLineEdit()
        self.scatter_on = QtWidgets.QPushButton("Select Entire Selection")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.to_scatter_label)
        layout.addWidget(self.to_scatter_line_edit)
        layout.addWidget(self.obj_to_scatter_btn)
        layout.addWidget(self.scatter_on_label)
        layout.addWidget(self.scatter_on_line_edit)
        layout.addWidget(self.scatter_on)
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

        self.obj_to_scatter_btn.clicked.connect(self.select_scatter)

        self.scatter_on.clicked.connect(self.select_to_scatter_verts)

        self.scatter_btn.clicked.connect(self.scatter)

    @QtCore.Slot()
    def scatter(self):
        self.scat.set_scale_and_rot_x(self.rand_scale_max_x.text(),
                                      self.rand_scale_min_x.text(),
                                      self.rand_rot_max_x.text(),
                                      self.rand_rot_min_x.text())
        self.scat.set_scale_and_rot_y(self.rand_scale_max_y.text(),
                                      self.rand_scale_min_y.text(),
                                      self.rand_rot_max_y.text(),
                                      self.rand_rot_min_y.text())
        self.scat.set_scale_and_rot_z(self.rand_scale_max_z.text(),
                                      self.rand_scale_min_z.text(),
                                      self.rand_rot_max_z.text(),
                                      self.rand_rot_min_z.text())
        self.scat.scatter_func()

    @QtCore.Slot()
    def select_to_scatter_obj(self):
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
        self.scale_max_x = 2
        self.scale_max_y = 2
        self.scale_max_z = 2
        self.scale_min_x = 0.5
        self.scale_min_y = 0.5
        self.scale_min_z = 0.5
        self.rot_max_x = 180
        self.rot_max_y = 180
        self.rot_max_z = 180
        self.rot_min_x = 0
        self.rot_min_y = 0
        self.rot_min_z = 0

    def set_scale_and_rot_x(self, scalemax, scalemin, rotmax, rotmin):
        self.scale_max_x = float(scalemax)
        self.scale_min_x = float(scalemin)
        self.rot_max_x = float(rotmax)
        self.rot_min_x = float(rotmin)

    def set_scale_and_rot_y(self, scalemax, scalemin, rotmax, rotmin):
        self.scale_max_y = float(scalemax)
        self.scale_min_y = float(scalemin)
        self.rot_max_y = float(rotmax)
        self.rot_min_y = float(rotmin)
        pass

    def set_scale_and_rot_z(self, scalemax, scalemin, rotmax, rotmin):
        self.scale_max_z = float(scalemax)
        self.scale_min_z = float(scalemin)
        self.rot_max_z = float(rotmax)
        self.rot_min_z = float(rotmin)
        pass

    def random_scale_instance(self, instance):
        random_x = self.random_change_in_direction(self.scale_max_x,
                                                   self.scale_min_x)
        random_y = self.random_change_in_direction(self.scale_max_y,
                                                   self.scale_min_y)
        random_z = self.random_change_in_direction(self.scale_max_z,
                                                   self.scale_min_z)
        cmds.scale(random_x, random_y, random_z, instance)

    def random_rotate_instance(self, instance):
        random_x = self.random_change_in_direction(self.rot_max_x,
                                                   self.rot_min_x)
        random_y = self.random_change_in_direction(self.rot_max_y,
                                                   self.rot_min_y)
        random_z = self.random_change_in_direction(self.rot_max_z,
                                                   self.rot_min_z)
        cmds.rotate(random_x, random_y, random_z, instance)

    def random_change_in_direction(self, max, min):
        scale_random = rand.random()
        old_range = (1 - 0)
        new_range = max - min
        scale_val = (((scale_random - 0) * new_range) / old_range) + min
        return scale_val

    def move_instance(self, instance, vert):
        pos_list = cmds.pointPosition(vert)
        pos_1 = pos_list[0]
        pos_2 = pos_list[1]
        pos_3 = pos_list[2]
        cmds.move(pos_1, pos_2, pos_3, instance)

    def select_verts_to_scatter_to(self):
        things_selected = cmds.ls(sl=True, flatten=True)
        things_selected = cmds.polyListComponentConversion(
            things_selected, toVertex=True)
        self.verts_to_scatter_on = cmds.filterExpand(things_selected, sm=31)
        return str(self.verts_to_scatter_on)

    def select_obj_to_scatter(self):
        self.selected_objs = cmds.ls(sl=True)
        self.obj_to_scatter = self.selected_objs[0]
        return str(self.obj_to_scatter)

    def scatter_func(self):
        for vertex in self.verts_to_scatter_on:
            self.instanced_obj = cmds.instance\
                (self.obj_to_scatter, smartTransform=True)
            self.random_scale_instance(self.instanced_obj)
            self.random_rotate_instance(self.instanced_obj)
            self.move_instance(self.instanced_obj, vertex)
