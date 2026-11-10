"""Permite importar los módulos al correr pytest desde la raíz del repo.

`src.pipeline_redes` (raíz en sys.path) para las pruebas del núcleo, y los
módulos por su nombre (`src/` en sys.path), como los importan los notebooks.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))
