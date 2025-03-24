from setuptools import setup

APP = ['app.py']
DATA_FILES = ['alarm.wav', 'icon.png']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5'],
    'includes': ['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QtMultimedia'],
    'plist': {
        'CFBundleName': 'PomodoroLab',
        'CFBundleDisplayName': 'PomodoroLab',
        'CFBundleVersion': "1.2.0",
        'CFBundleShortVersionString': "1.2.0",
        'CFBundleIdentifier': "com.arturylab.pomodorolab",
        'LSMinimumSystemVersion': "10.10",
        'CFBundleIconFile': 'icon.icns',
        'NSHumanReadableCopyright': 'Copyright © 2025 arturyLab. All rights reserved.',
        'NSPrincipalClass': 'NSApplication',
    }
}

setup(
    app=APP,
    name='PomodoroLab',
    version='1.2.0',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
