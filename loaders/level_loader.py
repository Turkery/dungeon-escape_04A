import json
from pathlib import Path
from typing import Any, Dict


class InvalidLevelError(Exception):
    """Exceptie aruncata atunci cand un fisier de nivel JSON nu respecta schema ceruta."""
    pass


def load_level_data(file_path: str | Path) -> Dict[str, Any]:
    """Citeste si valideaza structura unui nivel dintr-un fisier JSON."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Fisierul de nivel nu exista: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise InvalidLevelError(f"Format JSON invalid: {e}")

    # Validare chei obligatorii 
    required_keys = {"grid_size", "tile_size", "player_start", "exit", "walls", "doors", "keys", "enemies"}
    missing_keys = required_keys - set(data.keys())
    if missing_keys:
        raise InvalidLevelError(f"Lipseste configuratia obligatorie pentru: {missing_keys}")

    # Validare dimensiuni
    if not (isinstance(data["grid_size"], list) and len(data["grid_size"]) == 2):
        raise InvalidLevelError("Campul 'grid_size' trebuie sa fie o lista de doua numere [latime, inaltime].")

    if not isinstance(data["tile_size"], (int, float)) or data["tile_size"] <= 0:
        raise InvalidLevelError("Campul 'tile_size' trebuie sa fie un numar strict pozitiv.")

    # Validare player_start
    p_start = data["player_start"]
    if not (isinstance(p_start, list) and len(p_start) == 2):
        raise InvalidLevelError("Coordonata 'player_start' trebuie sa fie de forma [x, y].")

    # Validare exit
    exit_val = data["exit"]
    if isinstance(exit_val, dict):
        if "pos" not in exit_val or not (isinstance(exit_val["pos"], list) and len(exit_val["pos"]) == 2):
            raise InvalidLevelError("Campul 'exit' de tip dictionar trebuie sa contina 'pos': [x, y].")
    elif isinstance(exit_val, list):
        if len(exit_val) != 2:
            raise InvalidLevelError("Campul 'exit' de tip lista trebuie sa aiba lungimea 2: [x, y].")
    else:
        raise InvalidLevelError("Campul 'exit' trebuie sa fie fie [x, y], fie un dictionar cu cheia 'pos'.")
    
    # Validare usi si chei specifice 04A (trebuie sa aiba tipuri de culoare)
    for key_item in data["keys"]:
        if "color" not in key_item or "pos" not in key_item:
            raise InvalidLevelError("Fiecare cheie din 'keys' trebuie sa aiba 'color' si 'pos'.")

    for door_item in data["doors"]:
        if "color" not in door_item or "pos" not in door_item:
            raise InvalidLevelError("Fiecare usa din 'doors' trebuie sa aiba 'color' si 'pos'.")

    return data