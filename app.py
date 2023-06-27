import sys
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
from PySide6.QtGui import QPixmap, QImage, qRgb


class ImageInputApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pencil sketch app")

        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 500, 300)
        self.setFixedSize(600, 400)

        self.select_button = QPushButton("Select Image", self)
        self.select_button.setGeometry(50, 370, 200, 30)
        self.select_button.clicked.connect(self.select_image)

    def select_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Image files (*.png *.jpg *.jpeg *.gif)"])
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]

            # Convert image to pencil sketch
            sketch_image = self.convert_to_pencil_sketch(selected_file)

            # Display the sketch image
            self.display_image(sketch_image)

    def convert_to_pencil_sketch(self, image_path):
        # Load the image
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Invert the grayscale image
        inverted_image = cv2.bitwise_not(grayscale_image)

        # Apply Gaussian blur
        blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), 0)

        # Blend the grayscale image and the blurred image using the "color dodge" blending mode
        sketch_image = cv2.divide(grayscale_image, blurred_image, scale=256.0)

        return sketch_image

    def display_image(self, image):
        # Get the original image dimensions
        height, width = image.shape

        # Calculate the aspect ratio of the original image
        aspect_ratio = width / height

        # Calculate the maximum width and height based on the available space
        max_width = 500
        max_height = 300

        # Calculate the new width and height while maintaining the original aspect ratio
        new_width = min(max_width, int(max_height * aspect_ratio))
        new_height = min(max_height, int(max_width / aspect_ratio))

        # Resize the image to the new dimensions
        resized_image = cv2.resize(image, (new_width, new_height))

        # Convert the resized image to QImage
        q_image = QImage(
            resized_image.data, new_width, new_height, new_width, QImage.Format_Grayscale8
        )

        # Create QPixmap from QImage and display it in QLabel
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setGeometry(50, 50, new_width, new_height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_input_app = ImageInputApp()
    image_input_app.show()
    sys.exit(app.exec())
