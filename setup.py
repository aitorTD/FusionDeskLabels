from setuptools import setup

APP = ['cards.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['fpdf', 'tkinter'],
    'includes': ['fpdf'],
    'iconfile': 'app_icon.icns',  # Opcional: elimina o comenta esta línea si no tienes un ícono personalizado
    'plist': {
        'CFBundleName': 'GeneradorDeTarjetas',
        'CFBundleShortVersionString': '1.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'com.tuempresa.generadordetarjetas',
    },
}

setup(
    app=APP,
    name='GeneradorDeTarjetas',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)