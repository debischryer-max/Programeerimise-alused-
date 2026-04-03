import pubchempy as pcp


def fetch_compound(name):
    """Fetch a compound by name from PubChem. Returns (cid, smiles) or None."""
    compounds = pcp.get_compounds(name, "name")
    if compounds:
        c = compounds[0]
        return str(c.cid), c.isomeric_smiles
    return None
