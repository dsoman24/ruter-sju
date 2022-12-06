import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pandas as pd

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("hello")
        
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        df = pd.DataFrame([
           [0, 10], [5, 15], [2, 20], [15, 25], [4, 10],
        ], columns=['A', 'B'])
        df.plot(ax=sc.axes)
        # self.setCentralWidget(sc)
        hbox = QHBoxLayout()
        hbox.addWidget(sc)
        self.setLayout(hbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
