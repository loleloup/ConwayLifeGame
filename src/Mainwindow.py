from Tablewidget import *
from PyQt5.QtWidgets import QAction
import pathlib

class MainWind(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWind, self).__init__(parent)

        self.zoom_factor = DEFAULT_ZOOM_FACTOR
        self.current_directory = str(pathlib.Path(__file__).parent.parent.absolute())

        self._scene = QtWidgets.QGraphicsScene(self)
        self._view = QtWidgets.QGraphicsView(self._scene)

        self._tablew = TableWidget()
        self._tablew.setFixedSize(self._tablew.width * SQUARESIZE + (2 * MARGIN),
                                  self._tablew.height * SQUARESIZE + (2 * MARGIN))
        self._scene.addWidget(self._tablew)

        self.setCentralWidget(self._view)
        self.setMenuBar(self.buildMenuBar())

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

    def buildMenuBar(self):

        def registerMenuBarAction(menu, fun, display_name, icon_name = None):
            new_act = menu.addAction(display_name)                
            new_act.triggered.connect(fun)
            if icon_name:
                new_act.setIcon(Qt.QIcon(self.current_directory + "/icons/" + icon_name))

            # TODO : new_act.setShortcut()

        menu = QtWidgets.QMenuBar()

        registerMenuBarAction(menu, self._tablew.save, "save board", "save_button.png")
        registerMenuBarAction(menu, self._tablew.load, "load board", "open_button.png")
        registerMenuBarAction(menu, self.play, "play", "play_button.png")
        registerMenuBarAction(menu, self.pause, "pause", "pause_button.png")
        registerMenuBarAction(menu, self._tablew.next_step, "next step", "next_button.png")

        settingmenu = menu.addMenu("settings")
        settingmenu.setIcon(Qt.QIcon(self.current_directory + "/icons/settings_button.png"))
        
        registerMenuBarAction(settingmenu, self._tablew.resize_table, "resize grid")
        registerMenuBarAction(settingmenu, self._tablew.changedelay, "modify play speed")
        registerMenuBarAction(settingmenu, self._tablew.randomize, "randomize table")
        
        registerMenuBarAction(menu, self.zoom_in, "zoom in", "zoom-in.png")
        registerMenuBarAction(menu, self.zoom_out, "zoom out", "zoom-out.png")
        registerMenuBarAction(menu, self._tablew.clear, "erase", "erase_button.png")

        return menu


    def play(self):
        self._tablew.play()

    def pause(self):
        self._tablew.pause()

    @QtCore.pyqtSlot()
    def zoom_in(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(self.zoom_factor, self.zoom_factor)

        tr = self._view.transform() * scale_tr
        self._view.setTransform(tr)

    @QtCore.pyqtSlot()
    def zoom_out(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(self.zoom_factor, self.zoom_factor)

        scale_inverted, invertible = scale_tr.inverted()

        if invertible:
            tr = self._view.transform() * scale_inverted
            self._view.setTransform(tr)