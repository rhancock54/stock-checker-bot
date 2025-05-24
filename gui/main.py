from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QHBoxLayout, QScrollArea, QFormLayout
)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Checker")
        self.setGeometry(100, 100, 800, 600)

        tabs = QTabWidget()
        tabs.addTab(self.create_gpu_tab(), "GPU")
        tabs.addTab(self.create_tab("CPU"), "CPU")
        tabs.addTab(self.create_tab("RAM"), "RAM")
        tabs.addTab(self.create_tab("SSD"), "SSD")
        tabs.addTab(self.create_tab("PSU"), "PSU")
        tabs.addTab(self.create_tab("Motherboard"), "Motherboard")

        self.setCentralWidget(tabs)

    def create_gpu_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        form_layout = QFormLayout()

        form_layout.addRow("GPU Name:", QLineEdit())
        form_layout.addRow("Min Price:", QLineEdit())
        form_layout.addRow("Max Price:", QLineEdit())
        form_layout.addRow("Shipping Limit ($):", QLineEdit())

        add_button = QPushButton("+ Add another GPU")

        form_layout.addRow(add_button)
        scroll_content.setLayout(form_layout)
        scroll.setWidget(scroll_content)

        layout.addWidget(scroll)
        tab.setLayout(layout)
        return tab

    def create_tab(self, label_text):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"This is the {label_text} tab"))
        tab.setLayout(layout)
        return tab

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("gui/styles.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
