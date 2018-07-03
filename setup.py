import cx_Freeze
import sys
additional_mods = ['numpy.core._methods', 'numpy.lib.format']

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], 'includes':additional_mods,"excludes": ["tkinter"]}
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
bdist_msi_options = {
    'initial_target_dir': r'[PersonalFolder]\RecibosAdamant',
    # 'includes': ['atexit', 'PySide.QtNetwork'], # <-- this causes error
    }
	
cx_Freeze.setup(  name = "RecibosAdamant",
        version = "1.0",
        description = "Recibos Adamant",
        options = {
          'bdist_msi': bdist_msi_options,
          'build_exe': build_exe_options},
        executables = [cx_Freeze.Executable("RecibosPrado.py",shortcutName="Recibos Adamant",icon="adamant.ico", base=base)])