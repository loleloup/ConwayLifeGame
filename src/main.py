import PyQt5

from ConwayTable import *
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from VAR import *


class ResizeDialog(Qt.QDialog):

    def __init__(self, width, height):
        super().__init__()
        self.layout = QtWidgets.QFormLayout()

        self.width = QtWidgets.QSpinBox()
        self.height = QtWidgets.QSpinBox()
        self.width.setMaximum(2000)
        self.height.setMaximum(2000)
        self.width.setValue(width)
        self.height.setValue(height)

        self.layout.addRow(QtWidgets.QLabel("width"), self.width)
        self.layout.addRow(QtWidgets.QLabel("height"), self.height)
        cancel = QtWidgets.QPushButton("cancel")
        cancel.clicked.connect(self.reject)
        ok = QtWidgets.QPushButton("ok")
        ok.clicked.connect(self.accept)
        self.layout.addRow(cancel, ok)
        self.setLayout(self.layout)


    def get_width(self):
        return self.width.value()


    def get_height(self):
        return self.height.value()



class TableWidget(QtWidgets.QWidget):

    def __init__(self, x=100, y=100):
        super().__init__()
        self.playing = False
        self.width = x
        self.height = y
        self.disp_width = x * SQUARESIZE
        self.disp_height = y * SQUARESIZE
        self.table = ConwayTable(x, y)
        self.timer = Qt.QTimer()
        self.timer.timeout.connect(self.next_step)
        self.delay = 500

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor("black"), 1)
        brush = PyQt5.QtGui.QBrush(QtGui.QColor("black"))

        qp.setPen(pen)
        qp.setBrush(brush)
        for i in range(self.table.height):
            for j in range(self.table.width):
                if self.table.table[i][j]:
                    qp.setBrush(PyQt5.QtGui.QBrush(QtGui.QColor("black")))
                else:
                    qp.setBrush(PyQt5.QtGui.QBrush(QtGui.QColor("white")))
                qp.drawRect(SQUARESIZE * j + MARGIN, SQUARESIZE * i + MARGIN, 10, 10)

    def mousePressEvent(self, event):
        if not self.playing:
            bouton = event.button()
            if bouton == 1:
                pos = event.pos()
                if not (MARGIN < pos.x() < MARGIN + self.disp_width and MARGIN < pos.y() < MARGIN + self.disp_height):
                    return
                pos_x = (pos.x() - MARGIN) // 10
                pos_y = (pos.y() - MARGIN) // 10
                self.table.table[pos_y][pos_x] = not self.table.table[pos_y][pos_x]
                self.update()

    def next_step(self):
        self.table.update()
        self.update()

    def save(self):
        path = Qt.QFileDialog.getSaveFileName()[0]  # improve later with text files only or smth
        if path != '':
            self.table.save(path)

    def load(self):
        path = Qt.QFileDialog.getOpenFileName()[0]  # improve later with text files only or smth
        if path != '':
            with open(path) as file:

                size = file.readline().split(",")
                self.height = int(size[0])
                self.width = int(size[1])
                self.disp_width = self.width * SQUARESIZE
                self.disp_height = self.height * SQUARESIZE
                self.table = ConwayTable(self.width, self.height)
                self.table.load(file)
                self.update()

    def playpause(self):
        if not self.playing:
            self.playing = True
            self.timer.start(self.delay)
        else:
            self.playing = False
            self.timer.stop()

    def resize_table(self):
        dial = ResizeDialog(self.width, self.height)
        if dial.exec():
            if self.playing:
                self.playing = False
                self.timer.stop()
            width = dial.get_width()
            height = dial.get_height()
            self.table = ConwayTable(width, height)
            self.width = width
            self.height = height
            self.disp_width = width * SQUARESIZE
            self.disp_height = height * SQUARESIZE
            self.update()

    def changedelay(self):
        input = Qt.QInputDialog().getInt(None, "modify delay", "timer delay (ms)", self.delay, 50)
        if input[1]:
            self.delay = input[0]
            self.timer.setInterval(self.delay)

    def randomize(self):
        input = Qt.QInputDialog().getInt(None, "Randomize table", "rate", 50, 0, 100)
        if input[1]:
            self.table.randomize(input[0])

class MainWind(QtWidgets.QMainWindow):
    factor = 1.25

    def __init__(self, parent=None):
        super(MainWind, self).__init__(parent)

        self._scene = QtWidgets.QGraphicsScene(self)
        self._view = QtWidgets.QGraphicsView(self._scene)

        self._tablew = TableWidget()
        self._tablew.setFixedSize(self._tablew.width * SQUARESIZE + (2 * MARGIN),
                                  self._tablew.height * SQUARESIZE + (2 * MARGIN))
        self._scene.addWidget(self._tablew)

        self.setCentralWidget(self._view)

        menu = PyQt5.QtWidgets.QMenuBar()
        new_act = menu.addAction("save state")
        new_act.setIcon(Qt.QIcon("icons/save_button.png"))
        new_act.triggered.connect(self._tablew.save)

        new_act = menu.addAction("load state")
        new_act.setIcon(Qt.QIcon("icons/open_button.png"))
        new_act.triggered.connect(self._tablew.load)

        self.play_pause_button = menu.addAction("play-pause")
        self.play_pause_button.setIcon(Qt.QIcon("icons/play_button.png"))
        self.play_pause_button.triggered.connect(self.playpause)

        new_act = menu.addAction("next_step")
        new_act.setIcon(Qt.QIcon("icons/next_button.png"))
        new_act.triggered.connect(self._tablew.next_step)

        settingmenu = menu.addMenu("settings")
        settingmenu.setIcon(Qt.QIcon("icons/settings_button.png"))
        new_act = settingmenu.addAction("resize grid")
        new_act.triggered.connect(self._tablew.resize_table)
        new_act.triggered.connect(self.resetplay)
        new_act = settingmenu.addAction("modify play speed")
        new_act.triggered.connect(self._tablew.changedelay)
        new_act = settingmenu.addAction("randomize table")
        new_act.triggered.connect(self._tablew.randomize)


        new_act = menu.addAction("zoom_in")
        new_act.setIcon(Qt.QIcon("icons/zoom-in.png"))
        new_act.triggered.connect(self.zoom_in)

        new_act = menu.addAction("zoom_out")
        new_act.setIcon(Qt.QIcon("icons/zoom-out.png"))
        new_act.triggered.connect(self.zoom_out)

        self.setMenuBar(menu)

        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.ZoomIn),
            self._view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.zoom_in,
        )

        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.ZoomOut),
            self._view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.zoom_out,
        )

    def playpause(self):
        if self._tablew.playing:
            self.play_pause_button.setIcon(Qt.QIcon("icons/play_button.png"))
        else:
            self.play_pause_button.setIcon(Qt.QIcon("icons/pause_button.png"))
        self._tablew.playpause()

    def resetplay(self):
        self.play_pause_button.setIcon(Qt.QIcon("icons/play_button.png"))

    @QtCore.pyqtSlot()
    def zoom_in(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(MainWind.factor, MainWind.factor)

        tr = self._view.transform() * scale_tr
        self._view.setTransform(tr)

    @QtCore.pyqtSlot()
    def zoom_out(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(MainWind.factor, MainWind.factor)

        scale_inverted, invertible = scale_tr.inverted()

        if invertible:
            tr = self._view.transform() * scale_inverted
            self._view.setTransform(tr)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWind()
    ui.show()
    sys.exit(app.exec_())
