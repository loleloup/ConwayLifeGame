from Mainwindow import MainWind
from QtWidgets import QApplication

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = MainWind()
    ui.show()
    sys.exit(app.exec_())
