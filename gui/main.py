from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFormLayout, QGroupBox, QHBoxLayout, QCompleter, QTextEdit
)
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Checker")
        self.setGeometry(100, 100, 900, 700)

        self.gpu_suggestions = ["4070", "4070 Ti", "4080", "4080 Super", "4090", "5070", "5070 Ti", "9070", "9070 XT"]
        self.gpu_blocks = []

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

        self.add_gpu_input_block()

        self.add_button = QPushButton("+ Add another GPU")
        self.add_button.clicked.connect(self.add_gpu_input_block)

        self.track_button = QPushButton("Track Now")
        self.track_button.clicked.connect(self.track_gpus)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFixedHeight(150)

        self.form_layout.addWidget(self.add_button)
        self.form_layout.addWidget(self.track_button)
        self.form_layout.addWidget(self.log_output)

        self.scroll_content.setLayout(self.form_layout)
        self.scroll_area.setWidget(self.scroll_content)

        layout.addWidget(self.scroll_area)
        tab.setLayout(layout)
        return tab

    def add_gpu_input_block(self):
        block = QGroupBox("GPU Search Criteria")
        block_layout = QVBoxLayout()

        form = QFormLayout()
        name_input = QLineEdit()
        completer = QCompleter(self.gpu_suggestions)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        name_input.setCompleter(completer)

        min_price = QLineEdit()
        max_price = QLineEdit()
        shipping = QLineEdit()

        form.addRow("GPU Name:", name_input)
        form.addRow("Min Price:", min_price)
        form.addRow("Max Price:", max_price)
        form.addRow("Shipping Limit ($):", shipping)

        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda _, b=block: self.remove_gpu_block(b))

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(remove_btn)

        block_layout.addLayout(form)
        block_layout.addLayout(btn_layout)
        block.setLayout(block_layout)

        self.gpu_blocks.append((block, name_input, min_price, max_price, shipping))
        self.form_layout.insertWidget(len(self.gpu_blocks) - 1, block)

    def remove_gpu_block(self, block):
        if len(self.gpu_blocks) == 1:
            return
        for entry in self.gpu_blocks:
            if entry[0] == block:
                self.gpu_blocks.remove(entry)
                break
        self.form_layout.removeWidget(block)
        block.setParent(None)

    def track_gpus(self):
        self.log_output.clear()
        valid = True
        for idx, (_, name, min_price, max_price, shipping) in enumerate(self.gpu_blocks):
            try:
                name_text = name.text().strip()
                min_val = float(min_price.text().strip())
                max_val = float(max_price.text().strip())
                shipping_val = shipping.text().strip()
                shipping_val = float(shipping_val) if shipping_val else None
                if not name_text:
                    raise ValueError("GPU Name required")

                self.log_output.append(f"GPU {idx+1}: {name_text}, ${min_val} - ${max_val}, Shipping: ${shipping_val if shipping_val else 'Any'}")

            except ValueError as e:
                self.log_output.append(f"[Error] GPU {idx+1}: {str(e)}")
                valid = False

        if valid:
            self.log_output.append("✔ All inputs valid. Starting search... (TODO: Hook to backend)")

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
