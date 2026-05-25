import pytest

# Import main.pyw
# .pyw extension complicates things
import importlib.util
import sys
from pathlib import Path

main_file_path = Path(__file__).parent / "../main.pyw"
main_dir = str(main_file_path.parent)

# Inject this directory to the front of Python's search path
if main_dir not in sys.path:
    sys.path.insert(0, main_dir)

spec = importlib.util.spec_from_file_location("main", main_file_path)
main = importlib.util.module_from_spec(spec)
sys.modules["main"] = main
spec.loader.exec_module(main)
# Now main is can be used like a regular import
