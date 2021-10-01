from datetime import time
import sys
from os.path import basename
from functools import partial

import numpy as np
import matplotlib as mpl
import xarray as xr

mpl.use("Qt5Agg")

from PyQt5.QtWidgets import QApplication, QComboBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (
    QLineEdit,
    QDialog,
    QSlider,
    QPushButton,
    QToolBar,
    QHBoxLayout,
    QStatusBar,
    QVBoxLayout,
    QMessageBox,
    QLabel,
    QFileDialog,
)

from mpl.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from mpl.figure import Figure

from settings import *


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
        self.fileMenu.addAction("&Load roms_grd.nc", not_implemented)
        self.fileMenu.addAction("&Load roms_clm.nc", not_implemented)
        self.fileMenu.addAction("&Load roms_ini.nc", not_implemented)
        self.fileMenu.addAction("&Load roms_his.nc", not_implemented)
        self.fileMenu.addAction("&Quit", self.close)

        self.toolsMenu = self.menuBar().addMenu("&Plot")
        self.toolsMenu.addAction("&Hslice", not_implemented)
        self.toolsMenu.addAction("&Vslice", not_implemented)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        for key in RomsNCFiles.__dataclass_fields__.keys():
            tools.addAction(key.upper(), partial(self.openFile, f"*_{key}*.nc"))

    def _createSideBar(self):
        layout = QVBoxLayout()

        self.variables = QComboBox()
        layout.addWidget(self.variables)

        self.recs = QComboBox()
        layout.addWidget(self.recs)

        plot_types = QComboBox()
        plot_types.addItems(["contourf", "pcolormesh", "scatter"])
        layout.addWidget(plot_types)

        colorbars = QComboBox()
        colorbars.addItems(["black", "blue", "red", "green"])
        colorbars.activated[str].connect(self.set_plot_color)
        layout.addWidget(colorbars)

        alpha = QSlider(Qt.Horizontal)
        alpha.setValue(50)
        alpha.valueChanged[int].connect(self.set_plot_alpha)
        layout.addWidget(alpha)

        layout.addWidget(QPushButton("Vmin"))
        layout.addWidget(QPushButton("Vmax"))

        widget = QWidget()
        widget.setLayout(layout)
        widget.setFixedWidth(180)

        self.generalLayout.addWidget(widget)

    def _createMplCanvas(self):
        self.mplcanvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.update_plot("k")

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.mplcanvas, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.mplcanvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.generalLayout.addWidget(widget)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Ready...")
        self.setStatusBar(status)

    def openFile(self, pattern="*.nc"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "/source/roms-py/tests",
            f"NetCDF Files ({pattern});;All Files (*)",
            options=options,
        )
        if filename:
            self.hslice(filename)

    def hslice(self, filename, variable=None):
        ds = xr.open_dataset(filename)
        var = variable or getattr(firstvar, detect_roms_file(filename))
        da = ds[var]
        da = last2d(da)
        for ax in self.mplcanvas.figure.axes:
            ax.remove()

        self.mplcanvas.axes = self.mplcanvas.figure.add_subplot(111)

        self._plot = da.plot(ax=self.mplcanvas.axes)
        self.mplcanvas.draw()

        # update variables
        self.variables.clear()
        self.variables.addItems(ds.data_vars.keys())
        self.variables.setCurrentText(var)

        # update time records
        self.recs.clear()
        for dim in ds.dims.keys():
            if "time" in dim:
                times = [str(t).split(".")[0].replace("T", " ") for t in ds[dim].values]
                self.recs.addItems(times)
                self.recs.setCurrentText(var)
                break

    def set_colorbar(self, cbar):
        for line2d in self._plot:
            line2d.set_color(color)

        self.mplcanvas.draw()

    def set_plot_alpha(self, val):
        for line2d in self._plot:
            line2d.set_alpha(val / 100)

        self.mplcanvas.draw()


def detect_roms_file(filepath):
    for key in RomsNCFiles.__dataclass_fields__.keys():
        if key in basename(filepath):
            return key


def last2d(da):
    if da.ndim <= 2:
        return da

    slc = [0] * (da.ndim - 2)
    slc += [slice(None), slice(None)]
    slc = {d: s for d, s in zip(da.dims, slc)}

    return da.isel(**slc)


def not_implemented():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    # msg.setText("Error")
    msg.setInformativeText("Coming soon...")
    msg.setWindowTitle("Not found")
    msg.exec_()


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
