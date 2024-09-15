from ConwayTable import ConwayTable
from Qt import QDialog, QFileDialog, QTimer, QInputDialog
from QtGui import QPainter, QPen, QBrush, QColor
from QWidget import QWidget, QFormLayout, QSpinBox, QLabel, QPushButton
from VAR import MARGIN, SQUARESIZE, RAINBOW_FREQUENCY


class ResizeDialog(QDialog):
    def __init__(self, width, height):
        super().__init__()
        self.layout = QFormLayout()

        self.width = QSpinBox()
        self.height = QSpinBox()
        self.width.setMaximum(2000)
        self.height.setMaximum(2000)
        self.width.setValue(width)
        self.height.setValue(height)

        self.layout.addRow(QLabel("width"), self.width)
        self.layout.addRow(QLabel("height"), self.height)
        cancel = QPushButton("cancel")
        cancel.clicked.connect(self.reject)
        ok = QPushButton("ok")
        ok.clicked.connect(self.accept)
        self.layout.addRow(cancel, ok)
        self.setLayout(self.layout)

    def get_width(self):
        return self.width.value()

    def get_height(self):
        return self.height.value()


class TableWidget(QWidget):
    def __init__(self, x=100, y=100):
        super().__init__()
        self.playing = False
        self.width = x
        self.height = y
        self.disp_width = x * SQUARESIZE
        self.disp_height = y * SQUARESIZE
        self.table = ConwayTable(x, y)
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.delay = 500
        self.step = 0

    def paintEvent(self, event):
        qp = QPainter(self)
        pen = QPen(QColor("black"), 1)
        brush = QBrush(QColor("black"))

        qp.setPen(pen)
        qp.setBrush(brush)
        for i in range(self.table.height):
            for j in range(self.table.width):
                if self.table.table[i][j]:
                    this_color = QColor("white")
                    this_color.setHsv(
                        ((self.step + i + j) * RAINBOW_FREQUENCY) % 255, 255, 255
                    )
                    qp.setBrush(QBrush(this_color))
                else:
                    qp.setBrush(QBrush(QColor("white")))
                qp.drawRect(SQUARESIZE * j + MARGIN, SQUARESIZE * i + MARGIN, 10, 10)

    def mousePressEvent(self, event):
        if not self.playing:
            bouton = event.button()
            if bouton == 1:
                pos = event.pos()
                if not (
                    MARGIN < pos.x() < MARGIN + self.disp_width
                    and MARGIN < pos.y() < MARGIN + self.disp_height
                ):
                    return
                pos_x = (pos.x() - MARGIN) // 10
                pos_y = (pos.y() - MARGIN) // 10
                self.table.table[pos_y][pos_x] = not self.table.table[pos_y][pos_x]
                self.update()

    def next_step(self):
        self.step = self.step + 1
        self.table.update()
        self.update()

    def save(self):
        path = QFileDialog.getSaveFileName(None, "save file as", "saved", "*.tab")[
            0
        ]  # improve later with text files only or smth
        if path != "":
            self.table.save(path)

    def load(self):
        path = QFileDialog.getOpenFileName(None, "load file", "saved", "*.tab")[
            0
        ]  # improve later with text files only or smth
        if path != "":
            with open(path) as file:
                size = file.readline().split(",")
                self.height = int(size[0])
                self.width = int(size[1])
                self.disp_width = self.width * SQUARESIZE
                self.disp_height = self.height * SQUARESIZE
                self.table = ConwayTable(self.width, self.height)
                self.table.load(file)
                self.update()

    def toggle_play_pause(self):
        if not self.playing:
            self.play()
        else:
            self.pause()

    def play(self):
        self.playing = True
        self.timer.start(self.delay)

    def pause(self):
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
        input = QInputDialog().getInt(
            None, "modify delay", "timer delay (ms)", self.delay, 50
        )
        if input[1]:
            self.delay = input[0]
            self.timer.setInterval(self.delay)

    def randomize(self):
        input = QInputDialog().getInt(None, "Randomize table", "rate", 50, 0, 100)
        if input[1]:
            self.table.randomize(input[0])

    def clear(self):
        self.table = ConwayTable(self.width, self.height)
        self.update()
        self.playing = False
        self.timer.stop()
