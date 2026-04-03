import json
import glob
import os


_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(_ROOT_DIR, "input")


def list_chemicals_files():
    """Return all available *_chemicals.json files sorted by name."""
    return sorted(glob.glob(f"{INPUT_DIR}/*_chemicals.json"))


def load_chemicals(files):
    """Load and merge chemicals from a list of *_chemicals.json files."""
    merged = {}
    for path in files:
        with open(path) as f:
            merged.update(json.load(f))
    return merged


def select_chemicals_files():
    """Prompt the user to pick one or more chemicals files. Returns the selected list."""
    files = list_chemicals_files()
    if not files:
        print("No *_chemicals.json files found. Run 'Fetch chemicals' first.")
        return []

    print("Available chemical sets (enter numbers separated by spaces, e.g. 1 3):")
    for i, name in enumerate(files, 1):
        print(f"  {i}. {os.path.basename(name)}")

    while True:
        raw = input("\nSelect sets: ").strip()
        parts = raw.split()
        if parts and all(p.isdigit() and 1 <= int(p) <= len(files) for p in parts):
            return [files[int(p) - 1] for p in parts]
        print(f"Please enter numbers between 1 and {len(files)}, separated by spaces.")
