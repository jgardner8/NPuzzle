"""
cx_Freeze script to build executable that doesn't require Python.
Invoke with python setup.py build
"""

import sys
from cx_Freeze import setup, Executable

options = {
	"build_exe": {
		"build_exe": "bin/" + sys.platform,
	}
}

executables = [
	Executable(
		script = "main.py", 
		targetName = "search.exe" if sys.platform == "win32" else "search",
		appendScriptToExe = True,
        appendScriptToLibrary = False,
		base = None # only GUI applications require a base
	)
]

setup(
	name = "N-Puzzle",
	version = "1.0",
	description = "Solves a given N-Puzzle using a chosen search technique.",
	options = options,
	executables = executables
)