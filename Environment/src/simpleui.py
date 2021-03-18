import maya.OpenMayaUI as omui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

def maya_main_window()
    """return maya main window widget"""
    main_windows = omui.MQUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class SimpleUI(QtWidgets.QDialog):
    """simple UI class"""

    def __init__(self):
        """Instantiates a SimpleUI"""
        # This passes SimpleUI as an argument in super()
        # That futureproofs this code
        # super just instantiates the parent of SimpleUI
        super(SimpleUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("A Simple UI")
