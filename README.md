# PubChem Index Card Generator

Queries PubChem for a chemical compound by name and generates a PDF of landscape A6 index cards. Each compound gets two pages: the name on the front and the molecular structure drawing with SMILES on the back.

## Requirements

- Python 3.8 or later
- [pubchempy](https://github.com/mcs07/PubChemPy) — PubChem REST API client
- [rdkit](https://www.rdkit.org/) — cheminformatics library for molecule drawing
- [reportlab](https://www.reportlab.com/) — PDF generation

## Installation

Install all dependencies with pip:

```bash
pip install -r requirements.txt
```

> **Note:** On systems that enforce PEP 668 (e.g. Homebrew Python on macOS), you may need to use a virtual environment or pass `--break-system-packages`:
> ```bash
> pip install -r requirements.txt --break-system-packages
> ```

### Using a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python3 query_pubchem.py
```

You will be prompted to enter a chemical name:

```
Enter a chemical name: aspirin
Found 1 compound(s).
CC(=O)OC1=CC=CC=C1C(=O)O
PDF saved as aspirin.pdf
```

The output PDF is saved in the current directory, named after the compound (spaces replaced with underscores). Each compound found produces two pages in the PDF:

| Page | Content |
|------|---------|
| Front | Common name, IUPAC name, PubChem CID |
| Back | Molecular structure drawing, SMILES string |

## Files

| File | Description |
|------|-------------|
| `query_pubchem.py` | Entry point — prompts for input, queries PubChem, generates PDF |
| `index_card_pdf.py` | PDF formatting logic (`create_index_card_pdf` function) |
| `requirements.txt` | Python package dependencies |
