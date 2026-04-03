# Chemical Structure Quiz

A command-line quiz tool for learning to recognise organic chemistry structures. Given a molecular structure drawing, identify the correct chemical from a numbered list.

## How to use

### Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python3 main.py
```

### Menu options

#### 1. Fetch chemicals

Fetches chemical data from PubChem for a selected availability tier (green, orange, or blue) and saves it to `input/<tier>_chemicals.json`. Also generates SVG structure drawings for each compound into `chemical_structures/`.

Run this once per tier before creating any tests.

#### 2. Create test

Select one or more chemical tiers to draw from (e.g. `1 3` for green and blue). The program randomly picks 10 chemicals and generates one image per chemical showing:

- The molecular structure on the left
- A numbered list of all 10 chemical names on the right

Images and the answer key are saved to `tests/<tier>_test_<n>/`.

#### 3. Run test

Select a test to attempt. Each structure image is opened in your system viewer and you enter the number of the matching chemical name. Your results are displayed as a table and saved to `tests/<tier>_test_<n>/results_<datetime>.json`.

#### 4. Show results

Lists all completed test attempts across all tests. Select one to view a results table showing each chemical, the correct answer, your answer, and a pass/fail indicator.

#### 5. Exit

## Python packages used

| Package | Purpose |
|---------|---------|
| [pubchempy](https://github.com/mcs07/PubChemPy) | Queries the PubChem REST API to fetch compound data (CID, SMILES) by name |
| [rdkit](https://www.rdkit.org/) | Parses SMILES strings and renders molecular structure drawings as SVG and PNG |
| [Pillow](https://python-pillow.org/) | Composites the molecule image and name list into a single quiz image |
| [reportlab](https://www.reportlab.com/) | PDF generation (dependency of svglib) |
| [svglib](https://github.com/deeplook/svglib) | SVG rendering support |

## How Claude Code was used to write this package

This package was written entirely through conversation with Claude Code, Anthropic's AI coding assistant, without manually editing any source files.

The development process was iterative and conversational. It started with a simple script that queried PubChem for a single chemical by name. Through a series of natural language instructions, Claude Code incrementally built out the full application — refactoring the single script into a multi-file project, adding the quiz image generation, the interactive test runner, the results display, and the multi-tier chemical fetching.

Claude Code handled all structural decisions: splitting logic into separate modules (`pubchem.py`, `svg.py`, `chemicals_db.py`, etc.), moving files into `src/` and `input/` directories, updating all import paths, and keeping the code consistent across refactors. It also caught and fixed its own mistakes, such as a missing `import json` introduced during a refactor.

The README itself was written by Claude Code based on a brief from the author.
