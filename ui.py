from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, \
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QComboBox, QGridLayout
from parser import get_site_content


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Majestic Parser")
        outerLayout = QVBoxLayout()

        self.proxy_field = QLineEdit()
        self.domain_field = QLineEdit()
        self.button = QPushButton("get info")

        grid = QGridLayout()
        grid.addWidget(QLabel("proxy"), 0, 0)
        grid.addWidget(self.proxy_field, 0, 1)
        grid.addWidget(QLabel("domain"), 1, 0)
        grid.addWidget(self.domain_field, 1, 1)

        self.proxy_type = QComboBox()
        self.proxy_type.addItems(['HTTP', 'HTTPS'])

        grid.addWidget(self.proxy_type, 0, 2)
        grid.addWidget(self.button, 1, 2)

        self.citation_flow = QLineEdit()
        self.citation_flow.setReadOnly(True)
        self.trust_flow = QLineEdit()
        self.trust_flow.setReadOnly(True)

        grid_result = QGridLayout()
        grid_result.addWidget(QLabel("citation flow found"), 0, 0)
        grid_result.addWidget(QLabel("trust flow found"), 0, 1)
        grid_result.addWidget(self.citation_flow, 1, 0)
        grid_result.addWidget(self.trust_flow, 1, 1)

        self.error_message = QLabel()
        self.error_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.citation_flow.setFixedWidth(90)
        self.trust_flow.setFixedWidth(90)

        outerLayout.addLayout(grid)
        outerLayout.addLayout(grid_result)
        outerLayout.addWidget(self.error_message)
        self.button.clicked.connect(self.get_result)


        self.setLayout(outerLayout)


    def get_result(self):
        self.error_message.setText("Loading...")
        self.citation_flow.setText('')
        self.trust_flow.setText('')
        self.button.setEnabled(False)
        proxy = self.proxy_field.text().split(':')
        if len(proxy) not in (4, 2):
            self.error_message.setText("Wrong proxy format")
            self.button.setEnabled(True)
            return
        elif not self.domain_field.text():
            self.error_message.setText("Domain field is empty")
            self.button.setEnabled(True)
            return

        domain = self.domain_field.text()
        result = get_site_content(proxy, self.proxy_type.currentText(), domain)

        if result['error']:
            self.error_message.setText(result['error'])
            self.button.setEnabled(True)
        else:
            self.citation_flow.setText(str(result['citationFlow']))
            self.trust_flow.setText(str(result['trustFlow']))
            self.error_message.setText("Success")
            self.button.setEnabled(True)