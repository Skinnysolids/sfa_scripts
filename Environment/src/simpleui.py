from Pyside2 import QWidgets

class SimpleUI(QtWidgets.QDialog):
    """simple UI class"""

    def __init__(self):
        """Instantiates a SimpleUI"""
        # This passes SimpleUI as an argument in super()
        # That futureproofs this code
        # super just instantiates the parent of SimpleUI
        super(SimpleUI, self).__init__()
        self.setWindowTitle("A simple UI")
