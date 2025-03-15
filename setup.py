from setuptools import setup

APP = ['app.py']
DATA_FILES = [
    'alarm.wav',
    # Otros archivos de recursos
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5'],
    'iconfile': 'icon.icns',  # Ícono para macOS
    'plist': {
        'CFBundleName': 'PomodoroLab',
        'CFBundleDisplayName': 'PomodoroLab',
        'CFBundleVersion': "1.0.0",
        'CFBundleIdentifier': "com.arturylab.pomodorolab",
        'LSMinimumSystemVersion': "10.10",
    }
}

setup(
    app=APP,
    name='PomodoroLab',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
