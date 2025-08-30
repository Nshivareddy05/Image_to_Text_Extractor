import sys
import pytesseract
from PIL import Image
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QClipboard

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image → Text Extractor (OCR)")
        self.resize(600, 400)

        
        layout = QVBoxLayout()

       
        self.textbox = QTextEdit(self)
        self.textbox.setPlaceholderText("Extracted text will appear here...")

       
        btn_open = QPushButton("Open Image")
        btn_open.clicked.connect(self.load_image)

        btn_copy = QPushButton("Copy to Clipboard")
        btn_copy.clicked.connect(self.copy_text)

        btn_save = QPushButton("Save to File")
        btn_save.clicked.connect(self.save_text)

    
        layout.addWidget(btn_open)
        layout.addWidget(self.textbox)
        layout.addWidget(btn_copy)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            try:
                text = pytesseract.image_to_string(Image.open(path), lang="eng")
                self.textbox.setText(text.strip())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to extract text:\n{e}")

    def copy_text(self):
        text = self.textbox.toPlainText()
        if text.strip():
            QApplication.clipboard().setText(text, QClipboard.Clipboard)
            QMessageBox.information(self, "Copied", "Text copied to clipboard!")
        else:
            QMessageBox.warning(self, "Warning", "No text to copy.")

    def save_text(self):
        text = self.textbox.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Warning", "No text to save.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                QMessageBox.information(self, "Saved", f"Text saved to {path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec_())
