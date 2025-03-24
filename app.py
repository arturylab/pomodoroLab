"""
Pomodoro Timer Application with Session Management
Author: arturyLab
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QGridLayout,QPushButton, QTimeEdit,
                             QSpinBox, QFrame)
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtMultimedia import QSound

class PomodoroTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize window properties
        self.setWindowTitle('PomodoroLab')
        self.setFixedSize(400, 500)

        # Icon application
        self.setWindowIcon(QIcon("icon.png"))

        # Audio configuration
        self.sound_file = "alarm.wav"

        # Timer state management
        self.is_running = False        # Track if timer is active
        self.remaining_time = 0        # Seconds remaining in current session
        self.current_session = "work"  # Current session type (work/break)
        self.rounds_completed = 0      # Completed work sessions counter
        self.current_config_index = 0  # Initialize configuration index
        self.config = ['Classic', 'Deep Focus', '60/15 Technique', 'Short Sprint', 'Flex Mode']  # Configuration options

        # Initialize UI components and timer
        self.init_ui()
        self.reset_timer()
    
    def init_ui(self):
        """Initialize all user interface components"""
        # Main window setup
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Button styling
        self.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
            }
        """)

        # Session Status Display
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 20))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()
        main_layout.addWidget(self.status_label)

        # Main Timer Display Section
        self.timer_display = QLabel("")
        self.timer_display.setFont(QFont("Arial", 100))
        self.timer_display.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.timer_display)

        #Standard Configuration
        self.standard_label = QLabel("🍅 Classic")
        self.standard_label.setFont(QFont("Arial", 20))
        self.standard_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.standard_label)

        # Seetings Buttons Section
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)

        # Control Buttons Section (Forward)
        self.left_btn = QPushButton("◀︎")
        self.left_btn.setFixedSize(30, 30)  # Set fixed size for smaller circular shape
        self.left_btn.clicked.connect(self.toggle_config_left)
        self.left_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:pressed {
                background-color: #5AC66E;
            }
        """)
        btn_layout.addWidget(self.left_btn, alignment=Qt.AlignCenter)
        

        # Control Buttons Section (Play/Pause)
        self.play_pause_btn = QPushButton("Play")
        self.play_pause_btn.setFixedSize(60, 60)  # Set fixed size for smaller circular shape
        self.play_pause_btn.clicked.connect(self.toggle_timer)
        self.play_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                border-radius: 30px;
                font-size: 28px;
            }
            QPushButton:pressed {
                background-color: #5AC66E;
            }
        """)
        btn_layout.addWidget(self.play_pause_btn, alignment=Qt.AlignCenter)

        # Control Buttons Section (Forward)
        self.right_btn = QPushButton("►")
        self.right_btn.setFixedSize(30, 30)  # Set fixed size for smaller circular shape
        self.right_btn.clicked.connect(self.toggle_config_right)
        self.right_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:pressed {
                background-color: #5AC66E;
            }
        """)
        btn_layout.addWidget(self.right_btn, alignment=Qt.AlignCenter)

        main_layout.addWidget(btn_frame)

        # Settings Configuration Panel
        settings_frame = QFrame()
        settings_layout = QHBoxLayout(settings_frame)

        settings_frame.setStyleSheet("""
            QLabel {
            font-size: 16px; /* Increase font size for labels */
            }
            QTimeEdit, QSpinBox {
            font-size: 16px; /* Increase font size for buttons */
            }
        """)

        # Work Duration Configuration
        timer_layout = QGridLayout()
        timer_layout.addWidget(QLabel("Timer:"), 0, 0, alignment=Qt.AlignCenter)
        self.work_time = QTimeEdit()
        self.work_time.setDisplayFormat("mm:ss")
        self.work_time.setTime(QTime(0, 25, 0)) # Default work time 25 minutes (Classic)
        timer_layout.addWidget(self.work_time, 1, 0, alignment=Qt.AlignCenter)
        settings_layout.addLayout(timer_layout)

        # Break Duration Configuration
        break_layout = QGridLayout()
        break_layout.addWidget(QLabel("Break:"), 0 ,0, alignment=Qt.AlignCenter)
        self.break_time = QTimeEdit()
        self.break_time.setDisplayFormat("mm:ss")
        self.break_time.setTime(QTime(0, 5, 0)) # Default break time 5 minutes (Classic)
        break_layout.addWidget(self.break_time, 1, 0, alignment=Qt.AlignCenter)
        settings_layout.addLayout(break_layout)

        # Rounds Configuration
        rounds_layout = QGridLayout()
        rounds_layout.addWidget(QLabel("Rounds:"), 0, 0, alignment=Qt.AlignCenter)
        self.rounds = QSpinBox()
        self.rounds.setRange(1, 10) # Minimum 1, Maximum 10 rounds
        self.rounds.setValue(4) # Default rounds 4 (Classic)
        rounds_layout.addWidget(self.rounds, 1, 0, alignment=Qt.AlignCenter)
        settings_layout.addLayout(rounds_layout)

        main_layout.addWidget(settings_frame)

        # Connect settings changes
        self.work_time.timeChanged.connect(self.update_work_time)
        self.break_time.timeChanged.connect(self.update_break_time)
        self.rounds.valueChanged.connect(self.update_rounds)

        # System Control Buttons
        self.restart_btn = QPushButton("Restart")
        self.restart_btn.setFixedSize(60, 60)
        self.restart_btn.clicked.connect(self.reset_timer)
        self.restart_btn.setStyleSheet("""
            QPushButton {
            background-color: #DC3545;
            border-radius: 30px;
            font-size: 12px;
            font-weight: bold;
            }
            QPushButton:pressed {
            background-color: #E57373;
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
            self.left_btn.setEnabled(False)
            self.right_btn.setEnabled(False)

    def start_timer(self):
        """Start the timer and initialize session tracking"""
        self.is_running = True
        self.play_pause_btn.setText("⏸")
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
        self.play_pause_btn.setText("▶")
        self.timer.stop()
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
        self.left_btn.setEnabled(True)
        self.right_btn.setEnabled(True)

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

            if session_number == 1:
                emoji = "🚀"  # Motivational start
            elif session_number == total_rounds:
                emoji = "✅"  # Final session
            else:
                emoji = "🔥"  # Session in progress

            self.status_label.setText(f"{emoji} Session {session_number} of {total_rounds}")

        else:  # Break session
            break_number = self.rounds_completed

            if break_number == total_rounds:
                emoji = "🌿"  # Final long break
            else:
                emoji = "☕"  # Short break

            self.status_label.setText(f"{emoji} Break {break_number}")

    def update_standard_text(self):
        """Update standard label with current session information"""
        current_config = self.config[self.current_config_index]
        if current_config == "Classic":
            self.standard_label.setText(f"🍅 Classic")
            self.work_time.setTime(QTime(0, 25, 0))
            self.break_time.setTime(QTime(0, 5, 0))
            self.rounds.setValue(4)
        elif current_config == "Deep Focus":
            self.standard_label.setText(f"🎯 Deep Focus")
            self.work_time.setTime(QTime(0, 50, 0))
            self.break_time.setTime(QTime(0, 10, 0))
            self.rounds.setValue(3)
        elif current_config == "60/15 Technique":
            self.standard_label.setText(f"⏳ 60/15 Technique")
            self.work_time.setTime(QTime(0, 59, 59))
            self.break_time.setTime(QTime(0, 15, 0))
            self.rounds.setValue(2)
        elif current_config == "Short Sprint":
            self.standard_label.setText(f"⚡ Short Sprint")
            self.work_time.setTime(QTime(0, 15, 0))
            self.break_time.setTime(QTime(0, 3, 0))
            self.rounds.setValue(8)
        elif current_config == "Flex Mode":
            self.standard_label.setText(f"🔄 Flex Mode")
            self.work_time.setTime(QTime(0, 20, 0))
            self.break_time.setTime(QTime(0, 5, 0))
            self.rounds.setValue(6)

        # Update the timer display based on the new work time
        self.update_initial_time()

    def toggle_config_left(self):
        """Change config left"""
        self.current_config_index = (self.current_config_index - 1) % len(self.config)
        self.update_standard_text()

    def toggle_config_right(self):
        """Change config right"""
        self.current_config_index = (self.current_config_index + 1) % len(self.config)
        self.update_standard_text()

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