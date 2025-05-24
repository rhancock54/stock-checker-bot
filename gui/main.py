from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea, QFormLayout, QGroupBox, QHBoxLayout
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

        self.add_button = QPushButton("+ Add another GPU")
        self.add_button.clicked.connect(self.add_gpu_input_block)

        self.form_layout.addWidget(self.add_button)
        self.scroll_content.setLayout(self.form_layout)
        self.scroll_area.setWidget(self.scroll_content)

        layout.addWidget(self.scroll_area)
        tab.setLayout(layout)
        return tab

    def add_gpu_input_block(self):
        block = QGroupBox("GPU Search Criteria")
        block_layout = QVBoxLayout()

        form = QFormLayout()
        form.addRow("GPU Name:", QLineEdit())
        form.addRow("Min Price:", QLineEdit())
        form.addRow("Max Price:", QLineEdit())
        form.addRow("Shipping Limit ($):", QLineEdit())

        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda _, b=block: self.remove_gpu_block(b))
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(remove_btn)

        block_layout.addLayout(form)
        block_layout.addLayout(btn_layout)
        block.setLayout(block_layout)

        self.gpu_blocks.append(block)
        self.form_layout.insertWidget(len(self.gpu_blocks) - 1, block)

    def remove_gpu_block(self, block):
        if len(self.gpu_blocks) == 1:
            return  # Don't remove the last remaining block

        self.form_layout.removeWidget(block)
        block.setParent(None)
        self.gpu_blocks.remove(block)

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
