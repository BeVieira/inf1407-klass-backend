import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "klass_backend"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "klass_backend.settings")

app = get_wsgi_application()