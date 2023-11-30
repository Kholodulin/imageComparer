import sys
import cv2
from skimage.metrics import structural_similarity as ssim
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QFileDialog, QSizePolicy, QDialog

def convert_image_color(image):
    if image is not None:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return None

class ImageSimilarityApp(QWidget):
    def __init__(self):
        super().__init__()

        self.image1 = None
        self.image2 = None

        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(600, 400)
        self.setGeometry(100, 100, 700, 400)
        self.setWindowTitle('Калькулятор сходства изображений')
        
        self.label1 = QLabel(self)
        self.label1.setScaledContents(True)
        self.label1.setAlignment(Qt.AlignCenter) 
        self.label1.setMinimumSize(1, 1)

        self.label2 = QLabel(self)
        self.label2.setScaledContents(True)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setMinimumSize(1, 1)
        self.result_label = QLabel(self)

        load_image1_button = QPushButton('Загрузить изображение 1', self, font=QFont('Arial', 10))
        load_image1_button.clicked.connect(self.load_image1)

        load_image2_button = QPushButton('Загрузить изображение 2', self, font=QFont('Arial', 10))
        load_image2_button.clicked.connect(self.load_image2)

        calculate_button = QPushButton('Сравнить изображения', self, font=QFont('Arial', 10))
        calculate_button.clicked.connect(self.calculate_similarity)

        hbox_images = QHBoxLayout()
        hbox_images.addWidget(self.label1)
        hbox_images.addWidget(self.label2)
        spacer_item = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        hbox_images.addItem(spacer_item)

        vbox_buttons = QHBoxLayout()
        vbox_buttons.addWidget(load_image1_button)
        vbox_buttons.addWidget(load_image2_button)
        
        layout = QVBoxLayout(self)
        layout.addLayout(hbox_images)
        layout.addLayout(vbox_buttons)
        layout.addWidget(calculate_button)
        layout.addWidget(self.result_label)

    def display_image(self, image, label):
        if image is not None:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            label.setPixmap(pixmap)

    def load_image1(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp *.jpeg *.gif *.tiff *.ico)")
        file_dialog.exec()
        file_path = file_dialog.selectedFiles()[0] if file_dialog.result() == QDialog.Accepted else None
        if file_path:
            self.image1 = cv2.imread(file_path)
            self.image1 = convert_image_color(self.image1)
            self.display_image(self.image1, self.label1)

    def load_image2(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp *.jpeg *.gif *.tiff *.ico)")
        file_dialog.exec()
        file_path = file_dialog.selectedFiles()[0] if file_dialog.result() == QDialog.Accepted else None
        if file_path:
            self.image2 = cv2.imread(file_path)
            self.image2 = convert_image_color(self.image2)
            self.display_image(self.image2, self.label2)

    def calculate_similarity(self):
        if self.image1 is not None and self.image2 is not None:
            gray_image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
            gray_image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

            ssim_index, _ = ssim(gray_image1, gray_image2, full=True)
            percentage_similarity = ssim_index * 100

            self.result_label.setText(f"Процент схожести двух изображений: {percentage_similarity:.2f}%")

    def display_image(self, image, label):
        if image is not None:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSimilarityApp()
    window.show()
    sys.exit(app.exec())
