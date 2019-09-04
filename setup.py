from cx_Freeze import setup, Executable
import sys
import os
PYTHON_INSTALL_DIR = 'D:/Programs/Python/Python36'
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR,  'DLLs', 'tk86t.dll')
base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("main_gui.py", base=base)]

packages = ["pandas",'multiprocessing','numpy','scipy']
includes = ["pandas",'multiprocessing','numpy','scipy']
options = {
    'build_exe': {
        'includes':includes,
        'packages':packages,
    },
    # 'include_files':[
    #             os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
    #             os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
    #          ],

}

setup(
    name = "Document Extraction",
    options = options,
    version = "0.1",
    description = 'demo',
    executables = executables
)