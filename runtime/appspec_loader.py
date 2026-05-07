from pathlib import Path
import yaml


def load_appspec(path: str) -> dict:
    with open(Path(path), "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
