import math
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, \
    QGroupBox, QWidget, QGridLayout

import Kramers_Kronig_Calculation as kkc


class MainWindow(QMainWindow):
    def set_filename(self, x):
        self._filename = x

    def get_filename(self):
        return self._filename

    def __init__(self):
        # region setup
        super().__init__()
        self._filename = None
        self.title = "Kramers-Konig Relation"
        self.setWindowIcon(QIcon("Assets/project_icon_2.png"))
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 900
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        app.setStyleSheet('QLabel{font-size: 16pt;}'
                          'QComboBox{font-size: 12pt;}'
                          'QPushButton{font-size: 12pt;}'
                          'QSpinBox{font-size: 12pt;}'
                          'QDoubleSpinBox{font-size: 12pt;}'
                          'QCheckBox{font-size: 12pt;}'
                          'QGroupBox{border: 2px solid gray;border-radius: 5px;background: rgb(211, 218, 235);}'
                          'Selection-color: grey;')
        # endregion

        # region Widgets
        sub = QWidget(self)
        sub.setGeometry(self.left, self.top, self.width, self.height)
        layout = QGridLayout(self)

        file_sel = QLabel('Select File:', self)

        search = QPushButton('Search', self)
        search.clicked.connect(self.input_file)
        search.setFixedSize(300, 50)

        right_top_group = QGroupBox(self)

        run = QPushButton('Run Calculation', self)
        run.setFixedSize(300, 50)
        run.clicked.connect(self.start)

        bottom_text = QLabel("Acadia Physics 2023", self)
        bottom_text.setStyleSheet('font-size: 8pt;')

        logo_img = QLabel(self)
        self.logo_map = QPixmap('./Assets/logo.png')
        self.logo_resize = self.logo_map.scaled(450, 150, Qt.KeepAspectRatio)
        logo_img.setPixmap(self.logo_resize)
        logo_img.adjustSize()

        logo = QLabel('Kramers-Kronig Relation', self)
        logo.setStyleSheet('color: white;font-size: 16pt;')

        self.graph1_Title = QLabel("Input data Graph")
        self.graph2_Title = QLabel("Output data Graph")
        self.firstGraph = QLabel(self)
        self.secondGraph = QLabel(self)

        space = QLabel()

        layout.addWidget(space, 0, 0, 72, 0)  # left side
        layout.addWidget(space, 0, 0, 0, 96)  # top
        layout.addWidget(right_top_group, 1, 20, 2, -1)

        layout.addWidget(run, 3, 60, 2, 20)
        layout.addWidget(bottom_text, 70, 80, 2, 20)
        layout.addWidget(file_sel, 1, 30, 2, 20)
        layout.addWidget(search, 1, 60, 2, 20)
        layout.addWidget(logo_img, 1, 0, 2, 20)
        layout.addWidget(logo, 2, 0, 2, 20)
        layout.addWidget(self.graph1_Title, 6, 1, 2, 20)
        layout.addWidget(self.graph2_Title, 6, 55, 2, 20)
        layout.addWidget(self.firstGraph, 10, 0, 46, 46)
        layout.addWidget(self.secondGraph, 10, 55, 46, 46)

        sub.setLayout(layout)
        self.show()
        # endregion

    # region Functions
    def start(self):
        h = 1.05457 * math.pow(10, -34)
        de = (0.1 * math.pow(10, 13)) * h
        cshift = 1e-6

        f = open('{}'.format(window.get_filename()), 'r')
        x_axis = []
        spectra = []
        x_tick = []
        i = 0
        for line in f:
            i = i + 1
            line = line.strip().split('\t')
            x_axis.append(line[0])
            spectra.append(line[1])
            if i % 10 == 1:
                x_tick.append((line[0]))
        real = kkc.kkr((float(x_axis[1]) - float(x_axis[0])), window.get_filename(), cshift)
        spectra = np.array(spectra, np.float32)
        real = np.array(real, dtype=np.float32)
        x = np.array(x_tick, np.complex_)
        x_axis = np.array(x_axis, np.complex_)

        font = {'size': 8}
        plt.rc('font', **font)
        plt.plot(x_axis, real[:, 0, 0])
        plt.plot(x_axis, spectra)
        plt.xticks(x, x_tick, size='small')

        plt.savefig("./output.png", bbox_inches='tight', pad_inches=0.25)
        pixmap = QPixmap("./output.png")
        pixmap_resized = pixmap.scaled(525, 400)

        self.secondGraph.setPixmap(pixmap_resized)
        self.secondGraph.adjustSize()

    def input_file(self):
        self.firstGraph.clear()
        tmp = "./tmp.png"
        if os.path.isfile(tmp):
            os.remove(tmp)

        file_dialog = QFileDialog().getOpenFileName(self, 'Open file',
                                                    './Images_Input', "Text Files (*.txt)")

        image_path = file_dialog[0]
        res = os.path.isfile(image_path)
        if res:
            f = open('{}'.format(image_path), 'r')
            x_axis = []
            spectra = []
            x_tick = []
            i = 0
            for line in f:
                i = i + 1
                line = line.strip().split('\t')
                x_axis.append(line[0])
                spectra.append(line[1])
                if i % 10 == 1:
                    x_tick.append((line[0]))
            x = np.array(x_tick, np.complex_)
            spectra = np.array(spectra, np.float32)
            x_axis = np.array(x_axis, np.complex_)
            font = {'size': 8}
            plt.rc('font', **font)
            plt.plot(x_axis, spectra)
            plt.xticks(x, x_tick, size='small')
            plt.savefig("./tmp.png", bbox_inches='tight', pad_inches=0.25)
            pixmap = QPixmap("./tmp.png")
            pixmap_resized = pixmap.scaled(525, 400)
            self.firstGraph.setPixmap(pixmap_resized)
            self.firstGraph.adjustSize()
            window.set_filename(image_path)
        plt.clf()

    def set_output(self):
        output_path = QFileDialog().getExistingDirectory(self, None, "Select Folder")
        if output_path:
            window.set_output_path(output_path)
    # endregion


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
