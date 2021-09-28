import sys
from functools import partial

import numpy as np
import matplotlib

matplotlib.use("Qt5Agg")

from PyQt5.QtWidgets import QApplication, QComboBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel


from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("ROMSPyGUI")
        # self.setSize(800, 600)
        self.generalLayout = QHBoxLayout()
        # Set the central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.generalLayout)

        self._createMenu()
        self._createToolBar()
        self._createSideBar()
        self._createMplCanvas()
        self._createStatusBar()

    def _createMenu(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction("&Load roms_grd.nc", self.close)
        self.fileMenu.addAction("&Load roms_clm.nc", self.close)
        self.fileMenu.addAction("&Load roms_ini.nc", self.close)
        self.fileMenu.addAction("&Load roms_his.nc", self.close)
        self.fileMenu.addAction("&Exit", self.close)

        self.toolsMenu = self.menuBar().addMenu("&Plot")
        self.toolsMenu.addAction("&Hslice", self.close)
        self.toolsMenu.addAction("&Vslice", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction("GRD", self.close)
        tools.addAction("NUD", self.close)
        tools.addAction("INI", self.close)
        tools.addAction("BRY", self.close)
        tools.addAction("CLM", self.close)
        tools.addAction("HIS", self.close)
        tools.addAction("AVG", self.close)
        tools.addAction("QKS", self.close)
        tools.addAction("DIA", self.close)
        tools.addAction("FRC", self.close)
        tools.addAction("RIV", self.close)
        tools.addAction("TIDE", self.close)
        tools.addAction("Quit", self.close)

    def _createSideBar(self):
        layout = QVBoxLayout()

        variable = QComboBox()
        variable.addItems(["temp", "salt", "zeta"])
        layout.addWidget(variable)

        record = QComboBox()
        record.addItems(["2021-09-03 00:00", "2021-09-03 01:00", "2021-09-03 02:00"])
        layout.addWidget(record)

        plot_type = QComboBox()
        plot_type.addItems(["contourf", "pcolormesh", "scatter"])
        layout.addWidget(plot_type)

        colorbar = QComboBox()
        colorbar.addItems(["virids", "jet", "RdBu"])
        layout.addWidget(colorbar)

        layout.addWidget(QPushButton("Vmin"))
        layout.addWidget(QPushButton("Vmax"))

        widget = QWidget()
        widget.setLayout(layout)
        self.generalLayout.addWidget(widget)

    def _createMplCanvas(self):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(np.random.randn(500), alpha=0.4)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.generalLayout.addWidget(widget)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Ready...")
        self.setStatusBar(status)


class Controller:
    pass


# Client code
def main():
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    # palette = QPalette()
    # palette.setColor(QPalette.Window, QColor(53, 53, 53))
    # palette.setColor(QPalette.WindowText, Qt.white)
    # palette.setColor(QPalette.Base, QColor(25, 25, 25))
    # palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    # palette.setColor(QPalette.ToolTipBase, Qt.white)
    # palette.setColor(QPalette.ToolTipText, Qt.white)
    # palette.setColor(QPalette.Text, Qt.white)
    # palette.setColor(QPalette.Button, QColor(53, 53, 53))
    # palette.setColor(QPalette.ButtonText, Qt.white)
    # palette.setColor(QPalette.BrightText, Qt.red)
    # palette.setColor(QPalette.Link, QColor(42, 130, 218))
    # palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    # palette.setColor(QPalette.HighlightedText, Qt.black)
    # app.setPalette(palette)

    # Show the calculator's GUI
    view = Ui()
    view.show()
    # Create instances of the model and the controller
    # model = evaluateExpression
    # Controller(model=model, view=view)
    # Execute the calculator's main loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
