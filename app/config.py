import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.yaml"

with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

APP_CONFIG = config["app"]
DB_CONFIG = config["database"]
JWT_CONFIG = config["jwt"]