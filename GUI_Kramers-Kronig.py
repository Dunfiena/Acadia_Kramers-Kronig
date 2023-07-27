import sys
import os
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QFileDialog, \
    QSpinBox, QCheckBox, QGroupBox, QWidget, QTabWidget, QVBoxLayout, QGridLayout, QToolButton, QProgressBar, \
    QPlainTextEdit, QDoubleSpinBox
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
import numpy as np


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
        self.logo_resize = self.logo_map.scaled(300, 150, Qt.KeepAspectRatio)
        logo_img.setPixmap(self.logo_resize)
        logo_img.adjustSize()

        logo = QLabel('Kramers-Kronig Relation', self)
        logo.setStyleSheet('color: white;font-size: 20pt;')

        self.graph1_Title = QLabel("Input data Graph")
        self.graph2_Title = QLabel("Output data Graph")
        self.firstGraph = QLabel(self)
        self.secondGraph = QLabel(self)

        space = QLabel()

        layout.addWidget(space, 0, 0, 72, 0)  # left side
        layout.addWidget(space, 0, 0, 0, 96)  # top
        layout.addWidget(right_top_group, 1, 20, 2, -1)

        layout.addWidget(run, 1, 72, 2, 20)
        layout.addWidget(bottom_text, 70, 70, 2, 20)
        layout.addWidget(file_sel, 1, 30, 2, 20)
        layout.addWidget(search, 1, 45, 2, 20)
        layout.addWidget(logo_img, 1, 0, 2, 20)
        layout.addWidget(logo, 2, 0, 2, 20)
        layout.addWidget(self.graph1_Title, 16, 16, 2, 20)
        layout.addWidget(self.graph2_Title, 16, 32, 2, 20)


        sub.setLayout(layout)
        self.show()
        # endregion

    # region Functions
    def start(self):
        print('a')

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
            for line in f:
                line = line.strip().split('\t')
                x_axis.append((line[0]))
                spectra.append(line[1])
            spectra_plt = np.array(spectra, dtype=np.float32)
            plt.plot(spectra_plt)
            plt.savefig("./tmp.png")
            pixmap = QPixmap("./tmp.png")
            pixmap_resized = pixmap.scaled(650, 650, QtCore.Qt.KeepAspectRatio)
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
