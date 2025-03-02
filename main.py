import sys
from PyQt5.QtWidgets import QApplication
from gui_elements.mainGui_v2 import CustomDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CustomDialog()
    win.show()
    sys.exit(app.exec_())