"""
Preprocesses OCR-extracted markdown files for md2pptx conversion.

OCR artifacts fixed:
- Literal \\n characters → real newlines
- HTML slide number comments removed
- Copyright lines removed
- |Respuesta markers removed
- ### Notes: markers replaced by blank line (text becomes slide notes)
- H1 headings adjusted: first stays #, section dividers become ##, rest become ###
"""

import re
import sys

def preprocess(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replace literal \n (OCR artifact) with real newlines
    text = text.replace('\\n', '\n')

    # Remove HTML slide number comments
    text = re.sub(r'<!-- Slide number: \d+ -->\n?', '', text)

    # Remove copyright lines
    text = re.sub(r'Copyright[©®]?\s+\d{4}[-–]\d{4}.*?PeopleCert[^\n]*\n', '', text)

    # Remove |Respuesta / | Respuesta markers
    text = re.sub(r'^\| *Respuesta\n', '', text, flags=re.MULTILINE)

    # Replace ### Notes: with just a blank line so the following text becomes slide notes
    text = re.sub(r'\n+### Notes:\n', '\n\n', text)

    # Normalize non-breaking spaces
    text = text.replace('\xa0', ' ')

    # Adjust heading levels:
    # - Collect all H1 headings
    # - First H1 stays as # (module title)
    # - "Comprobación de conocimientos" becomes ##
    # - All other H1 → ###
    h1_count = [0]

    def replace_heading(m):
        title = m.group(1).strip()
        h1_count[0] += 1
        if h1_count[0] == 1:
            return f'# {title}'
        if 'comprobación de conocimientos' in title.lower():
            return f'## {title}'
        return f'### {title}'

    text = re.sub(r'^# (.+)$', replace_heading, text, flags=re.MULTILINE)

    # Ensure a blank line after every heading (md2pptx needs it to separate title from body)
    text = re.sub(r'^(#{1,6} .+)\n([^#\n])', r'\1\n\n\2', text, flags=re.MULTILINE)

    # Clean up more than 2 consecutive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    text = text.strip() + '\n'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f'Written: {output_path}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python preprocess_ocr.py input.md output.md')
        sys.exit(1)
    preprocess(sys.argv[1], sys.argv[2])
