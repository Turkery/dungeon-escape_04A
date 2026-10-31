import sys
from pathlib import Path
from core.engine import GameEngine
from loaders.level_loader import InvalidLevelError

def main():
    level_file = Path("data/level_1.json")
    
    try:
        engine = GameEngine(level_path=str(level_file))
        engine.run()
    except (FileNotFoundError, InvalidLevelError) as err:
        print(f"Eroare la pornirea jocului: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()