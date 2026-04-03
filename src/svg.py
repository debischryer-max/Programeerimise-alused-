import os

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

SVG_DIR = "chemical_structures"


def render_svg(cid, smiles):
    """Render a molecule SVG from SMILES and save it. Returns the file path or None."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    os.makedirs(SVG_DIR, exist_ok=True)
    drawer = rdMolDraw2D.MolDraw2DSVG(300, 300)
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    svg_path = os.path.join(SVG_DIR, f"{cid}.svg")
    with open(svg_path, "w") as f:
        f.write(drawer.GetDrawingText())
    return svg_path
