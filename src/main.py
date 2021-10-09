import PyQt5

from ConwayTable import *
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from VAR import *


class TableWidget(QtWidgets.QWidget):
    squaresize = 10
    squarecolor = "black"
    maxwidth = 2000
    maxheight = 2000

    def __init__(self, x=100, y=100):
        super().__init__()
        self.playing = False
        self.width = x
        self.height = y
        self.disp_width = x * self.squaresize
        self.disp_height = y * self.squaresize
        self.table = ConwayTable(x, y)
        self.timer = Qt.QTimer()
        self.timer.timeout.connect(self.next_step)

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
                qp.drawRect(self.squaresize * j + MARGIN, self.squaresize * i + MARGIN, 10, 10)

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
        # self.table.load()
        pass

    def playpause(self):
        if not self.playing:
            self.playing = True
            self.timer.start(500)
        else:
            self.playing = False
            self.timer.stop()

    def resize_table(self):
        pass


class MainWind(QtWidgets.QMainWindow):
    factor = 1.25

    def __init__(self, parent=None):
        super(MainWind, self).__init__(parent)

        self._scene = QtWidgets.QGraphicsScene(self)
        self._view = QtWidgets.QGraphicsView(self._scene)

        self._tablew = TableWidget()
        self._tablew.setFixedSize(self._tablew.width * self._tablew.squaresize + (2 * MARGIN),
                                  self._tablew.height * self._tablew.squaresize + (2 * MARGIN))
        self._scene.addWidget(self._tablew)

        self.setCentralWidget(self._view)

        menu = PyQt5.QtWidgets.QMenuBar()
        new_act = menu.addAction("save state")
        new_act.triggered.connect(self._tablew.save)

        new_act = menu.addAction("load state")
        new_act.triggered.connect(self._tablew.load)

        self.play_pause_button = menu.addAction("play-pause")
        self.play_pause_button.setIcon(Qt.QIcon("icons/play_button.png"))
        self.play_pause_button.triggered.connect(self.playpause)

        new_act = menu.addAction("next_step")
        #new_act.setIcon(Qt.QIcon("../next_button.jpg"))
        new_act.triggered.connect(self._tablew.next_step)

        settingmenu = menu.addMenu("settings")
        new_act = settingmenu.addAction("resize grid")
        new_act.triggered.connect(self._tablew.resize_table)

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
            self.play_pause_button.setIcon(Qt.QIcon("../play_button.jpg"))
        else:
            #self.play_pause_button.setIcon(Qt.QIcon("../pause_button.jpg"))
            pass
        self._tablew.playpause()

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