import json

from pubchem import fetch_compound
from svg import render_svg

CHEMICALS_FILE = "input/chemicals.json"
INPUT_DIR = "input"


def fetch_chemicals():
    with open(CHEMICALS_FILE) as f:
        data = json.load(f)

    colors = {k: v for k, v in data["meta"]["colors"].items() if k in data}
    color_list = list(colors.keys())

    print("Available tiers:")
    for i, color in enumerate(color_list, 1):
        print(f"  {i}. {color} — {colors[color]}")
    print(f"  {len(color_list) + 1}. Cancel")

    while True:
        choice = input("\nSelect a tier: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(color_list) + 1:
            break
        print(f"Please enter a number between 1 and {len(color_list) + 1}.")

    if int(choice) == len(color_list) + 1:
        return

    color = color_list[int(choice) - 1]
    names = data[color]
    output_file = f"{INPUT_DIR}/{color}_chemicals.json"

    print(f"\nFetching {len(names)} chemicals from PubChem...")
    results = {}
    for name in names:
        print(f"  {name}", end=" ", flush=True)
        result = fetch_compound(name)
        if result:
            cid, smiles = result
            results[cid] = {"name": name, "smiles": smiles}
            print(f"-> CID {cid}")
        else:
            print("-> not found")

    print(f"\nGenerating SVGs...")
    for cid, entry in results.items():
        svg_path = render_svg(cid, entry["smiles"])
        if svg_path:
            entry["svg"] = svg_path
        else:
            print(f"  Could not parse SMILES for {entry['name']}, skipping SVG")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. {len(results)}/{len(names)} chemicals saved to {output_file}")
