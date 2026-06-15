from pathlib import Path


def escape_pdf(text: str) -> str:
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


readme_path = Path('README.md')
text = readme_path.read_text(encoding='utf-8')
lines = text.splitlines()

content = ''
y = 760
for line in lines:
    content += f'BT /F1 12 Tf 72 {y} Td ({escape_pdf(line)}) Tj ET\n'
    y -= 14

stream_bytes = content.encode('latin-1', 'replace')
objects = [
    b'<< /Type /Catalog /Pages 2 0 R >>',
    b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>',
    f'<< /Length {len(stream_bytes)} >>\nstream\n'.encode('latin-1') + stream_bytes + b'\nendstream',
    b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
]

parts = [b'%PDF-1.4\n']
offsets = [0]
for i, obj in enumerate(objects, start=1):
    offsets.append(len(b''.join(parts)))
    parts.append(f'{i} 0 obj\n'.encode('latin-1'))
    parts.append(obj)
    parts.append(b'\nendobj\n')

xref_pos = len(b''.join(parts))
parts.append(b'xref\n')
parts.append(f'0 {len(objects) + 1}\n'.encode('latin-1'))
parts.append(b'0000000000 65535 f \n')
for off in offsets[1:]:
    parts.append(f'{off:010d} 00000 n \n'.encode('latin-1'))
parts.append(f'trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n'.encode('latin-1'))

Path('README.pdf').write_bytes(b''.join(parts))
print('Created README.pdf')
