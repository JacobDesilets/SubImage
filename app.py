from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QToolBar, \
    QFileDialog

# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)


# Create a Qt widget, which will be our window.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(400, 300))

        openAction = QAction("&Open", self)
        openAction.triggered.connect(self.open)

        img_label = QLabel()
        toolbar = QToolBar("toolbar")
        toolbar.addAction(openAction)

        main_layout = QVBoxLayout()
        self.addToolBar(toolbar)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def open(self):
        home_dir = str(Path.home())
        f = QFileDialog().getOpenFileName(self, "Open File", home_dir, 'Images (*.png *.jpeg *.jpg *.bmp *.gif)')

window = MainWindow()
window.show()

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
