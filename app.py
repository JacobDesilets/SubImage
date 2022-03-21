from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtGui import QAction, QPixmap, QImage, QPalette
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QToolBar, \
    QFileDialog, QScrollArea, QSizePolicy, QRubberBand

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

        self.original_pixmap = None
        self.rubber_band = None
        self.rubber_band_origin = None

        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.open)

        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.triggered.connect(self.zoom_in)

        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.triggered.connect(self.zoom_out)

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.img_label.setScaledContents(True)
        self.img_label.setBackgroundRole(QPalette.ColorRole.Dark)

        toolbar = QToolBar("toolbar")
        toolbar.addAction(open_action)
        toolbar.addAction(zoom_in_action)
        toolbar.addAction(zoom_out_action)

        self.addToolBar(toolbar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.img_label)
        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Dark)

        self.setCentralWidget(self.scroll_area)

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(400, 300))

    def open(self):
        home_dir = str(Path.home())
        f, _ = QFileDialog().getOpenFileName(self, "Open File", home_dir, 'Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        print(f)
        img = QImage(f)
        self.img_label.setPixmap(QPixmap.fromImage(img))
        self.original_pixmap = QPixmap.fromImage(img)
        size = QSize(img.size())
        self.img_label.resize(size)

    def resize(self, scale):

        old_pixmap = self.img_label.pixmap()
        old_pixmap_size = old_pixmap.size()

        new_pixmap = self.original_pixmap.scaled(int(old_pixmap_size.width() * scale), int(old_pixmap_size.height() * scale))

        self.img_label.setPixmap(new_pixmap)

        self.img_label.resize(self.img_label.pixmap().size())

    def zoom_in(self):
        self.resize(1.1)

    def zoom_out(self):
        self.resize(0.9)

    def mousePressEvent(self, event):
        self.rubber_band_origin = event.pos()
        if not self.rubber_band:
            self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.rubber_band.setGeometry(QRect(self.rubber_band_origin, QSize()))
        self.rubber_band.show()

    def mouseMoveEvent(self, event):
        self.rubber_band.setGeometry(QRect(self.rubber_band_origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.rubber_band.hide()
        print(QRect(self.rubber_band_origin, event.pos()).normalized().intersects(self.img_label.pixmap().rect()))


window = MainWindow()
window.show()

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
