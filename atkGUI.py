import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFormLayout, QHBoxLayout
)

class AttackTab(QWidget):
    def __init__(self, attack_type, script_name):
        super().__init__()
        self.attack_type = attack_type
        self.script_name = script_name
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        #user input
        form_layout = QFormLayout()
        self.target_ip = QLineEdit()
        self.target_port = QLineEdit()
        form_layout.addRow("Target IP:", self.target_ip)
        form_layout.addRow("Target Port:", self.target_port)

        #atk button
        self.attack_button = QPushButton(f"Launch {self.attack_type} Attack")
        self.attack_button.clicked.connect(self.launch_attack)

        #output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        layout.addLayout(form_layout)
        layout.addWidget(self.attack_button)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self.output_display)

        self.setLayout(layout)

    def launch_attack(self):
        ip = self.target_ip.text()
        port = self.target_port.text()

        try:
            #EXAMPLE - TO BE REPLACED
            result = subprocess.run(
                ["python3", self.script_name, ip, port],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.output_display.setText(result.stdout + "\n" + result.stderr)
        except Exception as e:
            self.output_display.setText(f"Error running attack: {str(e)}")

class AttackGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DoS/DDoS Attack Launcher")
        self.setGeometry(100, 100, 700, 500)
        self.init_ui()

    def init_ui(self):
        tabs = QTabWidget()

        #tab creation - placeholder scripts/names - TO BE REPLACED
        tabs.addTab(AttackTab("VM Network-Based", "attack_vm_network.py"), "VM Network")
        tabs.addTab(AttackTab("VM Host-Based", "attack_vm_host.py"), "VM Host")
        tabs.addTab(AttackTab("Container Network-Based", "attack_container_network.py"), "Container Network")
        tabs.addTab(AttackTab("Container Host-Based", "attack_container_host.py"), "Container Host")

        self.setCentralWidget(tabs)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        with open("atkrTheme.qss", "r") as file:
            app.setStyleSheet(file.read())
    except Exception as e:
        print(f"Error loading theme: {e}")

    window = AttackGUI()
    window.show()
    sys.exit(app.exec_())