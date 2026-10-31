from typing import Dict, Any, List, Tuple

class Level:
    """Reține datele și starea logică a unui nivel de joc, independent de randare."""
    def __init__(self, raw_data: Dict[str, Any]):
        self.grid_width: int = raw_data["grid_size"][0]
        self.grid_height: int = raw_data["grid_size"][1]
        self.tile_size: int = raw_data["tile_size"]
        
        self.player_start: Tuple[int, int] = tuple(raw_data["player_start"])
        self.exit_data: Dict[str, Any] = raw_data["exit"]
        
        self.walls: List[Tuple[int, int]] = [tuple(w) for w in raw_data.get("walls", [])]
        self.doors: List[Dict[str, Any]] = raw_data.get("doors", [])
        self.keys: List[Dict[str, Any]] = raw_data.get("keys", [])
        self.enemies: List[Dict[str, Any]] = raw_data.get("enemies", [])

        if isinstance(raw_data["exit"], dict):
            self.exit_pos: Tuple[int, int] = tuple(raw_data["exit"]["pos"])
            self.exit_condition = raw_data["exit"].get("requires_all_doors_open", False)
        else:
            self.exit_pos: Tuple[int, int] = tuple(raw_data["exit"])
            self.exit_condition = False