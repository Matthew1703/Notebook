# pylint: skip-file
import sys
from pathlib import Path

# Добавляем src в PYTHONPATH
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
