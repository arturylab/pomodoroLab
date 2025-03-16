"""
Pomodoro Timer Application with Session Management
Author: arturyLab
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QGridLayout,QPushButton, QTimeEdit,
                             QSpinBox, QFrame)
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QSound

class PomodoroTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize window properties
        self.setWindowTitle('PomodoroLab App')
        self.setFixedSize(400, 400)

        # Audio configuration
        self.sound_file = "alarm.wav"

        # Timer state management
        self.is_running = False        # Track if timer is active
        self.remaining_time = 0        # Seconds remaining in current session
        self.current_session = "work"  # Current session type (work/break)
        self.rounds_completed = 0      # Completed work sessions counter

        # Initialize UI components and timer
        self.init_ui()
        self.reset_timer()
    
    def init_ui(self):
        """Initialize all user interface components"""
        # Main window setup
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Main Timer Display Section
        self.timer_display = QLabel("50:00")
        self.timer_display.setFont(QFont("Arial", 100))
        self.timer_display.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.timer_display)

        # Session Status Display
        self.status_label = QLabel("Working")
        self.status_label.setFont(QFont("Arial", 22))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()
        main_layout.addWidget(self.status_label)

        # Control Buttons Section
        self.play_pause_btn = QPushButton("Play")
        self.play_pause_btn.clicked.connect(self.toggle_timer)
        self.play_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #4b88a2;
                border-radius: 6px;
                min-width: 10em;
                padding: 6px;
            }
            QPushButton:pressed {
                background-color: #67a5bf;
            }
        """)
        main_layout.addWidget(self.play_pause_btn, alignment=Qt.AlignCenter)

        # Settings Configuration Panel
        settings_frame = QFrame()
        settings_layout = QHBoxLayout(settings_frame)

        # Work Duration Configuration
        timer_layout = QGridLayout()
        timer_layout.addWidget(QLabel("Timer:"), 0, 0, alignment=Qt.AlignCenter)
        self.work_time = QTimeEdit()
        self.work_time.setDisplayFormat("mm:ss")
        self.work_time.setTime(QTime(0, 50, 0)) # Default work time 50 minutes
        timer_layout.addWidget(self.work_time, 1, 0, alignment=Qt.AlignCenter)
        settings_layout.addLayout(timer_layout)

        # Break Duration Configuration
        break_layout = QGridLayout()
        break_layout.addWidget(QLabel("Break:"), 0 ,0, alignment=Qt.AlignCenter)
        self.break_time = QTimeEdit()
        self.break_time.setDisplayFormat("mm:ss")
        self.break_time.setTime(QTime(0, 10, 0)) # Default brake time 10 minutes
        break_layout.addWidget(self.break_time, 1, 0, alignment=Qt.AlignCenter)
        settings_layout.addLayout(break_layout)

        # Rounds Configuration
        rounds_layout = QGridLayout()
        rounds_layout.addWidget(QLabel("Rounds:"), 0, 0, alignment=Qt.AlignCenter)
        self.rounds = QSpinBox()
        self.rounds.setRange(1, 10) # Minimum 1, Maximum 10 rounds
        self.rounds.setValue(3) # Default rounds 2
        rounds_layout.addWidget(self.rounds, 1, 0, alignment=Qt.AlignCenter)
        settings_layout.addLayout(rounds_layout)

        main_layout.addWidget(settings_frame)

        # Connect settings changes
        self.work_time.timeChanged.connect(self.update_work_time)
        self.break_time.timeChanged.connect(self.update_break_time)
        self.rounds.valueChanged.connect(self.update_rounds)

        # System Control Buttons
        self.restart_btn = QPushButton("Restart")
        self.restart_btn.clicked.connect(self.reset_timer)
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #bb0a21;
                border-radius: 6px;
                min-width: 10em;
                padding: 6px;
            }
            QPushButton:pressed {
                background-color: #d43c50;
            }
        """)
        main_layout.addWidget(self.restart_btn, alignment=Qt.AlignCenter)

        # Timer Mechanisn Setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Developer Information
        self.developer_label = QLabel("Developed by arturyLab")
        self.developer_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.developer_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                padding: 2px;
            }
        """)
        main_layout.addWidget(self.developer_label)

    def toggle_timer(self):
        """Toggle between start and pause states"""
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()

    def start_timer(self):
        """Start the timer and initialize session tracking"""
        self.is_running = True
        self.play_pause_btn.setText("Pause")
        self.timer.start(1000) # Update every second (1000ms)

        self.status_label.show()
        self.update_status_text()

        # Lock configuration controls during active session
        self.work_time.setEnabled(False)
        self.break_time.setEnabled(False)
        self.rounds.setEnabled(False)

    def pause_timer(self):
        """Pause the timer and unlock configuration controls"""
        self.is_running = False
        self.play_pause_btn.setText("Play")
        self.timer.stop()

        # Hide status and enable configuration edits
        self.status_label.hide()
        self.work_time.setEnabled(True)
        self.break_time.setEnabled(True)
        self.rounds.setEnabled(True)

    def reset_timer(self):
        """Reset all timer values to initial state"""
        self.pause_timer()
        self.current_session = "work"
        self.rounds_completed = 0
        self.remaining_time = self._calculate_remaining_time()
        self.update_status_text()
        self.update_display()

    def update_initial_time(self):
        """Calculate initial time based on current session type"""
        if self.current_session == "work":
            time = self.work_time.time()
        else:
            time = self.break_time.time()
        
        # Convert QTime to total seconds
        self.remaining_time = time.minute() * 60 + time.second()
        self.update_display()

    def update_timer(self):
        """Update timer countdown and check for session completion"""
        self.remaining_time -= 1

        if self.remaining_time <= 0:
            self.handle_session_end()

        self.update_display()

    def handle_session_end(self):
        """Manage session transitions and round completion"""
        QSound.play(self.sound_file) # Play alarm
        if self.current_session == "work":
            self.rounds_completed += 1
            
            # Check if all rounds completed
            if self.rounds_completed >= self.rounds.value():
                self.reset_timer()
                self.status_label.hide()
                return
            self.current_session = "break"
        else:
            self.current_session = "work"

        self.update_status_text()
        self.update_initial_time()
    
    def update_status_text(self):
        """Update status label with current session information"""
        total_rounds = self.rounds.value()
        if self.current_session == "work":
            session_number = self.rounds_completed + 1
            self.status_label.setText(f"Session {session_number} of {total_rounds}")
        else:
            break_number = self.rounds_completed
            self.status_label.setText(f"Break {break_number}")

    def update_display(self):
        """Update main timer display with formatted time"""
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_display.setText(f"{minutes:02}:{seconds:02}")
    
    def update_work_time(self):
        """Update work time when QTimeEdit is modified"""
        self.remaining_time = self._calculate_remaining_time()

    def update_break_time(self):
        """Update break time when QTimeEdit is modified"""
        # Only update if the timer is in "break" mode
        if self.current_session == "break":
            self.remaining_time = self._calculate_remaining_time()

    def update_rounds(self):
        """Update the number of rounds when QSpinBox is modified"""
        # No immediate action required, will apply in the next cycle
        pass

    def _calculate_remaining_time(self):
        """Calculate remaining time based on the current session"""
        if self.current_session == "work":
            return self.work_time.time().minute() * 60 + self.work_time.time().second()
        else:
            return self.break_time.time().minute() * 60 + self.break_time.time().second()


if __name__ == "__main__":
    # Initialize and run the application
    app = QApplication(sys.argv)
    window = PomodoroTimer()
    window.show()
    sys.exit(app.exec_())