import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFormLayout, QHBoxLayout, QSpinBox
)

class AttackTab(QWidget):
    def __init__(self, attack_type, script_path):
        super().__init__()
        self.attack_type = attack_type
        self.script_path = script_path
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # User input
        form_layout = QFormLayout()
        self.target_ip = QLineEdit()
        self.target_port = QLineEdit()
        self.duration = QSpinBox()
        self.duration.setRange(1, 300)  # 1-300 seconds
        self.duration.setValue(30)  # Default 30 seconds
        
        form_layout.addRow("Target IP:", self.target_ip)
        form_layout.addRow("Target Port:", self.target_port)
        form_layout.addRow("Duration (s):", self.duration)

        # Attack button
        self.attack_button = QPushButton(f"Launch {self.attack_type} Attack")
        self.attack_button.clicked.connect(self.launch_attack)

        # Output display
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
        duration = str(self.duration.value())

        try:
            # Launch attack script with parameters
            result = subprocess.run(
                ["python3", self.script_path, ip, port, duration],
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
        self.setWindowTitle("Attack Launcher")
        self.setGeometry(100, 100, 700, 500)
        self.init_ui()

    def init_ui(self):
        tabs = QTabWidget()

        # VM-based attacks
        vm_attack_path = os.path.join("attacks", "vm", "syn_fldVM.py")
        tabs.addTab(AttackTab("VM Network", vm_attack_path), "VM Network")
        
        # Container-based attacks
        container_net_path = os.path.join("attacks", "container", "syn_fldContainer.py")
        container_cpu_path = os.path.join("attacks", "container", "cpu_exhaust_container.py")
        tabs.addTab(AttackTab("Container Network", container_net_path), "Container Network")
        tabs.addTab(AttackTab("Container CPU", container_cpu_path), "Container CPU")

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