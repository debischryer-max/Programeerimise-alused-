import sys
import pubchempy as pcp
from index_card_pdf import create_index_card_pdf

name = input("Enter a chemical name: ").strip()
compounds = pcp.get_compounds(name, 'name')

print(f"Found {len(compounds)} compound(s).")

if not compounds:
    sys.exit(0)

for compound in compounds:
    print(compound.smiles)

pdf_filename = f"{name.replace(' ', '_')}.pdf"
create_index_card_pdf(name, compounds, pdf_filename)
print(f"PDF saved as {pdf_filename}")
