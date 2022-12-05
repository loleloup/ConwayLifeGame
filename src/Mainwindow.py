from Tablewidget import *
import pathlib

class MainWind(QtWidgets.QMainWindow):
    factor = 1.25
    current_directory = str(pathlib.Path(__file__).parent.parent.absolute())
    def __init__(self, parent=None):
        super(MainWind, self).__init__(parent)

        self._scene = QtWidgets.QGraphicsScene(self)
        self._view = QtWidgets.QGraphicsView(self._scene)

        self._tablew = TableWidget()
        self._tablew.setFixedSize(self._tablew.width * SQUARESIZE + (2 * MARGIN),
                                  self._tablew.height * SQUARESIZE + (2 * MARGIN))
        self._scene.addWidget(self._tablew)

        self.setCentralWidget(self._view)

        menu = QtWidgets.QMenuBar()
        new_act = menu.addAction("save state")
        new_act.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/save_button.png"))
        new_act.triggered.connect(self._tablew.save)

        new_act = menu.addAction("load state")
        new_act.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/open_button.png"))
        new_act.triggered.connect(self._tablew.load)

        self.play_pause_button = menu.addAction("play-pause")
        self.play_pause_button.setIcon(Qt.QIcon(MainWind.current_directory + "/icons\play_button.png"))
        self.play_pause_button.triggered.connect(self.playpause)

        new_act = menu.addAction("next_step")
        new_act.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/next_button.png"))
        new_act.triggered.connect(self._tablew.next_step)

        settingmenu = menu.addMenu("settings")
        settingmenu.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/settings_button.png"))
        new_act = settingmenu.addAction("resize grid")
        new_act.triggered.connect(self._tablew.resize_table)
        new_act.triggered.connect(self.resetplay)
        new_act = settingmenu.addAction("modify play speed")
        new_act.triggered.connect(self._tablew.changedelay)
        new_act = settingmenu.addAction("randomize table")
        new_act.triggered.connect(self._tablew.randomize)

        new_act = menu.addAction("zoom_in")
        new_act.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/zoom-in.png"))
        new_act.triggered.connect(self.zoom_in)

        new_act = menu.addAction("zoom_out")
        new_act.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/zoom-out.png"))
        new_act.triggered.connect(self.zoom_out)

        new_act = menu.addAction("erase")
        new_act.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/erase-button.png"))
        new_act.triggered.connect(self._tablew.clear)

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
            self.play_pause_button.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/play_button.png"))
        else:
            self.play_pause_button.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/pause_button.png"))
        self._tablew.playpause()

    def resetplay(self):
        self.play_pause_button.setIcon(Qt.QIcon(MainWind.current_directory + "/icons/play_button.png"))

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