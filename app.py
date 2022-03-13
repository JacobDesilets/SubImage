from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QPixmap, QImage, QPalette
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QToolBar, \
    QFileDialog, QScrollArea, QSizePolicy

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



        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.open)

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.img_label.setScaledContents(True)

        self.img_label.setBackgroundRole(QPalette.ColorRole.Base)

        toolbar = QToolBar("toolbar")
        toolbar.addAction(open_action)

        self.addToolBar(toolbar)


        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.img_label)
        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Base)

        self.setCentralWidget(self.scroll_area)

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(400, 300))

    def open(self):
        home_dir = str(Path.home())
        f, _ = QFileDialog().getOpenFileName(self, "Open File", home_dir, 'Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        print(f)
        img = QImage(f)
        self.img_label.setPixmap(QPixmap.fromImage(img))
        size = QSize(img.size())
        self.img_label.setMinimumSize(size)


window = MainWindow()
window.show()

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
