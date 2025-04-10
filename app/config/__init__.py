import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("FLASK_ENV", "dev")

if env == "prod":
    from .prod import *  # Импорт всех настроек из prod.py
elif env == "test":
    from .test import *  # Импорт всех настроек из test.py
else:
    from .dev import *  # Импорт всех настроек из dev.py
