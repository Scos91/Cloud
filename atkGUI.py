import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFormLayout, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
import threading
import datetime

class AttackTab(QWidget):
    class OutputEmitter(QObject):
        outputSignal = pyqtSignal(str)
        buttonResetSignal = pyqtSignal()

    def __init__(self, attack_type, script_name, input_fields):
        super().__init__()
        self.attack_type = attack_type
        self.script_name = script_name
        self.input_fields = input_fields
        self.emitter = self.OutputEmitter()
        self.emitter.outputSignal.connect(self.append_output)
        self.emitter.buttonResetSignal.connect(self.reset_button)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.inputs = {}

        #user input
        form_layout = QFormLayout()
        for label, default in self.input_fields:
            field = QLineEdit()
            field.setPlaceholderText(default)
            field.setText(default)
            field.setStyleSheet("color: gray;")
            self.inputs[label] = field
            form_layout.addRow(label + ":", field)

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

    def append_output(self, text):
        self.output_display.append(text)

    def launch_attack(self):
        self.output_display.clear()

        self.attack_button.setEnabled(False)
        original_text = self.attack_button.text()
        self.attack_button.setText("Launching...")

        def runAtk():
            try:
                args = [field.text() for field in self.inputs.values()]
                result = subprocess.run(
                    ["sudo", "python3", self.script_name] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output = result.stdout + "\n" + result.stderr
            except Exception as e:
                output = f"Error running attack: {str(e)}"

            self.emitter.outputSignal.emit(output)

            self.emitter.buttonResetSignal.emit()
            self.log_attack(args, output)
            # def reset_button():
            #     self.attack_button.setEnabled(True)
            #     self.attack_button.setText(original_text)
            # QTimer.singleShot(0, reset_button)

            # self.output_display.append(output)

        thread = threading.Thread(target=runAtk)
        thread.start()

        # self.output_display.clear()
        # try:
        #     args = [field.text() for field in self.inputs.values()]
        #     result = subprocess.run(
        #         ["sudo", "python3", self.script_name] + args,
        #         stdout=subprocess.PIPE,
        #         stderr=subprocess.PIPE,
        #         text=True
        #     )
        #     self.output_display.setText(result.stdout + "\n" + result.stderr)
        # except Exception as e:
        #     self.output_display.setText(f"Error running attack: {str(e)}")

    def reset_button(self):
        self.attack_button.setEnabled(True)
        self.attack_button.setText(f"Launch {self.attack_type} Attack")

    def log_attack(self, args, output):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (
            f"---\n"
            f"Timestamp: {timestamp}\n"
            f"Attack Type: {self.attack_type}\n"
            f"Script: {self.script_name}\n"
            f"Arguments: {args}\n"
            f"Result:\n{output}\n"
        )
        with open("attackLog.txt", "a") as log_file:
            log_file.write(log_entry)

class AttackGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attack GUI - Cloud Security Project")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        tabs = QTabWidget()

        #tab creation
        tabs.addTab(AttackTab("VM Network-Based", "synAtkVm.py", [("Target IP", "192.168.1.157"), ("Target Port", "80"), ("Packet Rate", "1000"), ("Duration (seconds)", "10")]), "VM Network")
        tabs.addTab(AttackTab("VM Host-Based", "burnCPU_VmHost.py", [("Number of Processes", "2"), ("Duration (seconds)", "10")]), "VM Host")
        tabs.addTab(AttackTab("Container Network-Based", "httpFlood_Container.py", [("Container IP", "192.168.1.157"), ("Port", "8080"), ("Number of Requests", "10000"), ("Concurrency", "100"), ("Request Path", "/")]), "Container Network")
        tabs.addTab(AttackTab("Container Host-Based", "frkBombHost_Container.py", [("Number of Forks", "50"), ("Delay Between Forks", "0.1")]), "Container Host")

        self.setCentralWidget(tabs)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        with open("atkrTheme_redteam.qss", "r") as file:
            app.setStyleSheet(file.read())
    except Exception as e:
        print(f"Error loading theme: {e}")

    window = AttackGUI()
    window.show()
    sys.exit(app.exec_())