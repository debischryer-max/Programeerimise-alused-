import io
from rdkit import Chem
from rdkit.Chem import Draw
from svglib.svglib import svg2rlg
from reportlab.lib.pagesizes import A6, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

_PAGE_SIZE = landscape(A6)
_PAGE_WIDTH = _PAGE_SIZE[0] - 2 * cm
_PAGE_HEIGHT = _PAGE_SIZE[1] - 2 * cm
# SimpleDocTemplate adds 6 pt of padding on each side of the frame
_FRAME_PAD = 6
_USABLE_WIDTH = _PAGE_WIDTH - 2 * _FRAME_PAD
_USABLE_HEIGHT = _PAGE_HEIGHT - 2 * _FRAME_PAD

def _build_styles():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CenteredTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        'CenteredSubtitle',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=8,
        textColor='grey',
    )
    return title_style, subtitle_style


def _draw_molecule(smiles):
    """Return a ReportLab Drawing (SVG) of the molecule, or None if SMILES is invalid."""
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return None
    d2d = Draw.MolDraw2DSVG(600, 600)
    try:
        Draw.SetACS1996Mode(d2d.drawOptions(), Draw.MeanBondLength(mol))
    except Exception:
        d2d.drawOptions().bondLineWidth = 2.0
    d2d.DrawMolecule(mol)
    d2d.FinishDrawing()
    svg_bytes = io.BytesIO(d2d.GetDrawingText().encode("utf-8"))
    return svg2rlg(svg_bytes)


def create_index_card_pdf(name, compounds, pdf_filename):
    """Create a landscape A6 index-card PDF for the given list of PubChem compounds.

    Each compound gets two pages:
      - Front: chemical name, IUPAC name, and PubChem CID
      - Back:  molecule drawing and SMILES string
    """
    title_style, subtitle_style = _build_styles()

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=_PAGE_SIZE,
        topMargin=1 * cm,
        bottomMargin=1 * cm,
        leftMargin=1 * cm,
        rightMargin=1 * cm,
    )

    story = []

    for i, compound in enumerate(compounds):
        smiles = compound.smiles

        # --- Front page: name ---
        story.append(Spacer(1, 2 * cm))
        story.append(Paragraph(name.title(), title_style))
        if compound.iupac_name:
            story.append(Spacer(1, 0.5 * cm))
            story.append(Paragraph(f"IUPAC: {compound.iupac_name}", subtitle_style))
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(f"PubChem CID: {compound.cid}", subtitle_style))
        story.append(PageBreak())

        # --- Back page: drawing ---
        mol_drawing = _draw_molecule(smiles)
        if mol_drawing:
            # Scale to fill the usable frame area, preserving aspect ratio.
            scale = min(_USABLE_WIDTH / mol_drawing.width, _USABLE_HEIGHT / mol_drawing.height)
            mol_drawing.width *= scale
            mol_drawing.height *= scale
            mol_drawing.transform = (scale, 0, 0, scale, 0, 0)
            story.append(mol_drawing)
        else:
            story.append(Paragraph("(Could not parse SMILES)", subtitle_style))

        story.append(PageBreak())

    doc.build(story)
