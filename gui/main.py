from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea, QFormLayout, QGroupBox
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

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.form_layout = QVBoxLayout()

        self.gpu_blocks = []
        self.add_gpu_input_block()

        add_button = QPushButton("+ Add another GPU")
        add_button.clicked.connect(self.add_gpu_input_block)

        self.form_layout.addWidget(add_button)
        self.scroll_content.setLayout(self.form_layout)
        self.scroll_area.setWidget(self.scroll_content)

        layout.addWidget(self.scroll_area)
        tab.setLayout(layout)
        return tab

    def add_gpu_input_block(self):
        block = QGroupBox("GPU Search Criteria")
        form = QFormLayout()
        form.addRow("GPU Name:", QLineEdit())
        form.addRow("Min Price:", QLineEdit())
        form.addRow("Max Price:", QLineEdit())
        form.addRow("Shipping Limit ($):", QLineEdit())
        block.setLayout(form)

        self.gpu_blocks.append(block)
        self.form_layout.insertWidget(len(self.gpu_blocks) - 1, block)

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
