from Mainwindow import *


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWind()
    ui.show()
    sys.exit(app.exec_())
