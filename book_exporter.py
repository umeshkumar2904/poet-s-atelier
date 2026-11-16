from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from poetry_engine import PoetryBookPlan

def build_book_docx(plan: PoetryBookPlan, poems: list[dict], author_name: str) -> BytesIO:
    doc = Document()
    poem_lookup = {p["title"].strip().lower(): p["content"] for p in poems}

    # Title Page
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title_p.add_run(f"\n\n\n{plan.suggested_book_title.upper()}\n")
    run.bold = True
    run.font.size = Pt(26)

    sub_run = title_p.add_run(f"{plan.subtitle}\n\n")
    sub_run.italic = True
    sub_run.font.size = Pt(14)

    auth_run = title_p.add_run(f"By {author_name}")
    auth_run.font.size = Pt(14)
    doc.add_page_break()

    # Preface
    doc.add_heading("Preface", level=1)
    doc.add_paragraph(plan.preface)
    doc.add_page_break()

    # Chapters & Poems
    for chapter in plan.chapters:
        ch_head = doc.add_heading(f"Chapter {chapter.chapter_number}: {chapter.chapter_title}", level=1)
        ch_head.alignment = WD_ALIGN_PARAGRAPH.CENTER

        epigraph = doc.add_paragraph(f'"{chapter.chapter_epigraph}"')
        epigraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        epigraph.runs[0].italic = True
        doc.add_page_break()

        for p_title in chapter.poem_titles:
            doc.add_heading(p_title, level=2)
            body = poem_lookup.get(p_title.strip().lower(), "[Poem text not found]")
            poem_para = doc.add_paragraph(body)
            poem_para.paragraph_format.line_spacing = 1.25
            doc.add_page_break()

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer