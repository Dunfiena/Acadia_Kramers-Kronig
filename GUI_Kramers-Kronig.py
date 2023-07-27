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
    def __init__(self):
        super().__init__()
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
        
        self.show()


class create_window(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

    def input_file(self):
        self.image_label.clear()
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
            self.image_label.setPixmap(pixmap_resized)
            self.image_label.adjustSize()
            window.set_filename(image_path)
        plt.clf()

    def set_output(self):
        output_path = QFileDialog().getExistingDirectory(self, None, "Select Folder")
        if output_path:
            window.set_output_path(output_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
