import sys
import subprocess
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFormLayout, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import QTimer

class DefenseGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Defensive Monitoring, Detection, and Mitigation Tool")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

        #placeholder monitoring vars
        self.monitoring = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        #thresholds
        threshold_layout = QFormLayout()
        self.cpu_threshold = QLineEdit("90")
        self.mem_threshold = QLineEdit("80")
        threshold_layout.addRow("CPU Threshold (%):", self.cpu_threshold)
        threshold_layout.addRow("Memory Threshold (%):", self.mem_threshold)
        layout.addLayout(threshold_layout)

        #buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Monitoring")
        self.start_button.clicked.connect(self.toggle_monitoring)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Monitoring")
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        #sys outputs
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        layout.addWidget(QLabel("System Metrics / Alerts:"))
        layout.addWidget(self.output_display)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def toggle_monitoring(self):
        self.monitoring = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.output_display.append("[INFO] Monitoring started...")
        self.timer.start(2000) #2sec check

    def stop_monitoring(self):
        self.monitoring = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.output_display.append("[INFO] Monitoring stopped.")
        self.timer.stop()

    def update_metrics(self):
        #placeholder - simulate reading/detection
        # thread = threading.Thread(target=self.simulate_monitoring_check)
        # thread.start()

        self.simulate_monitoring_check()

    def simulate_monitoring_check(self):
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent

        msg = f"CPU: {cpu}%, Memory: {mem}%"
        self.output_display.append(msg)

        cpu_thresh = float(self.cpu_threshold.text())
        mem_thresh = float(self.mem_threshold.text())

        if cpu > cpu_thresh:
            self.output_display.append("[ALERT] CPU usage exceeded threshold!")
            self.perform_mitigation("CPU")
        if mem > mem_thresh:
            self.output_display.append("[ALERT] Memory usage exceeded threshold!")
            self.perform_mitigation("Memory")

    def perform_mitigation(self, reason):
        #placeholder - mitigation logic (block IP, kill proc, etc.)
        self.output_display.append(f"[MITIGATION] Taking action due to {reason} spike...")
        
        #log to DB - Add here?
        QMessageBox.warning(self, "Mitigation Triggered", f"Mitigation performed for: {reason}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #load theme
    try:
        with open("defTheme.qss", "r") as file:
            app.setStyleSheet(file.read())
    except Exception as e:
        print(f"Theme not loaded: {e}")

    window = DefenseGUI()
    window.show()
    sys.exit(app.exec_())