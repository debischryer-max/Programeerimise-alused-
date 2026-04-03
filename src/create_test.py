import json
import os
import random
from io import BytesIO

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image, ImageDraw, ImageFont

from chemicals_db import select_chemicals_files, load_chemicals

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(_ROOT_DIR, "tests")
MOL_SIZE = 300
IMG_WIDTH = 620
IMG_HEIGHT = 340
TEXT_X = MOL_SIZE + 20


def create_test():
    files = select_chemicals_files()
    if not files:
        return
    chemicals = load_chemicals(files)

    selected = random.sample(list(chemicals.items()), 10)

    name_list = [data["name"] for _, data in selected]
    random.shuffle(name_list)
    name_to_number = {name: i + 1 for i, name in enumerate(name_list)}

    tiers = "_".join(os.path.basename(f).replace("_chemicals.json", "") for f in files)
    prefix = f"{tiers}_test_"
    existing = [d for d in os.listdir(TESTS_DIR) if d.startswith(prefix)]
    numbers = [int(d[len(prefix):]) for d in existing if d[len(prefix):].isdigit()]
    next_num = max(numbers, default=0) + 1
    test_dir = os.path.join(TESTS_DIR, f"{prefix}{next_num}")
    os.makedirs(test_dir, exist_ok=True)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except OSError:
        font = ImageFont.load_default()

    test_answers = {}

    for cid, data in selected:
        mol = Chem.MolFromSmiles(data["smiles"])
        if mol is None:
            print(f"  Could not parse SMILES for {data['name']}, skipping")
            continue

        drawer = rdMolDraw2D.MolDraw2DCairo(MOL_SIZE, MOL_SIZE)
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        mol_img = Image.open(BytesIO(drawer.GetDrawingText()))

        composite = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), "white")
        mol_y = (IMG_HEIGHT - MOL_SIZE) // 2
        composite.paste(mol_img, (0, mol_y))

        draw = ImageDraw.Draw(composite)
        draw.line([(MOL_SIZE + 10, 10), (MOL_SIZE + 10, IMG_HEIGHT - 10)], fill="#cccccc", width=1)

        line_height = (IMG_HEIGHT - 20) // 10
        for i, name in enumerate(name_list, 1):
            y = 10 + (i - 1) * line_height + (line_height - 16) // 2
            draw.text((TEXT_X, y), f"{i}.  {name}", fill="black", font=font)

        filename = f"{cid}.png"
        composite.save(os.path.join(test_dir, filename))
        test_answers[filename] = name_to_number[data["name"]]

    with open(os.path.join(test_dir, "test.json"), "w") as f:
        json.dump(test_answers, f, indent=2)

    print(f"Test created in {test_dir}/")


