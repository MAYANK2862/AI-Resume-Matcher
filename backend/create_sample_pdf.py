"""
Generates clean sample PDF resumes for drag-and-drop testing.
Uses raw PDF 1.4 specification without external heavy libraries.
"""
import os
from sample_data import SAMPLE_RESUMES


def create_simple_pdf(text: str, output_path: str):
    """Generates a valid, well-formed minimal PDF 1.4 document containing the text."""
    lines = text.strip().split('\n')

    # Build PDF content stream
    content_lines = ["BT", "/F1 10 Tf", "14 TL", "50 750 Td"]
    for line in lines[:55]:  # fit on page 1
        clean_line = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        if clean_line.strip():
            content_lines.append(f"({clean_line}) Tj")
        content_lines.append("T*")
    content_lines.append("ET")
    stream_content = "\n".join(content_lines).encode('latin-1', 'replace')

    stream_len = len(stream_content)

    objects = []
    # 1: Catalog
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    # 2: Pages
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    # 3: Page
    objects.append(
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    )
    # 4: Stream Content
    objects.append(
        f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode('latin-1') +
        stream_content +
        b"\nendstream\nendobj\n"
    )
    # 5: Font
    objects.append(
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    )

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode('latin-1'))
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode('latin-1'))

    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode('latin-1')
    )

    with open(output_path, "wb") as f:
        f.write(pdf)


def generate_all_samples():
    sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_resumes")
    os.makedirs(sample_dir, exist_ok=True)

    for s in SAMPLE_RESUMES:
        filename = f"{s['candidate_name'].replace(' ', '_')}_Resume.pdf"
        out_path = os.path.join(sample_dir, filename)
        create_simple_pdf(s["raw_text"], out_path)
        print(f"Generated sample PDF: {out_path}")


if __name__ == "__main__":
    generate_all_samples()

