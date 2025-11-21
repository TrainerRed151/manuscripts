import re
import sys
from bs4 import BeautifulSoup

# Mapping Unicode to LaTeX (without quotes — handled by csquotes)
UNICODE_LATEX = {
    '…': r'\ldots',
    '“‘': r'``\hspace{0pt}`',    '’”': r"'\hspace{0pt}''",
    '“': '``',      '”': "''",
    '‘': '`',       '’': "'",
    '–': '--',      '—': '---',
    'ç': r'\c{c}',  'Ç': r'\c{C}',
    'ñ': r'\~n',    'Ñ': r'\~N',
    'œ': r'\oe ',   'Œ': r'\OE ',
    'à': r'\`a',    'À': r'\`A',
    'á': r"\'a",    'Á': r"\'A",
    'â': r'\^a',    'Â': r'\^A',
    'ä': r'\"a',    'Ä': r'\"A',
    'ã': r'\~a',    'Ã': r'\~A',
    'å': r'\r a',   'Å': r'\r A',
    'ā': r'\=a',    'Ā': r'\=A',
}


def replace_unicode_latex(text):
    for uni, latex in UNICODE_LATEX.items():
        text = text.replace(uni, latex)
    return text


def html_to_latex(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Headings
    for i in range(1, 7):
        for tag in soup.find_all(f'h{i}'):
            latex_tag = 'chapter' if i == 1 else f'section'*(i-1)
            tag.string = '\\{}{{{}}}'.format(latex_tag, tag.get_text())

    # Bold and Italic
    for tag in soup.find_all(['b', 'strong']):
        tag.string = '\\textbf{{{}}}'.format(tag.get_text())
    for tag in soup.find_all(['i', 'em']):
        tag.string = '\\textit{{{}}}'.format(tag.get_text())

    # Lists
    for ul in soup.find_all('ul'):
        items = [f'\\item {li.get_text()}' for li in ul.find_all('li')]
        ul.string = '\\begin{itemize}\n' + '\n'.join(items) + '\n\\end{itemize}'
    for ol in soup.find_all('ol'):
        items = [f'\\item {li.get_text()}' for li in ol.find_all('li')]
        ol.string = '\\begin{enumerate}\n' + '\n'.join(items) + '\n\\end{enumerate}'

    # Links
    for tag in soup.find_all('a', href=True):
        tag.string = '\\href{{{}}}{{{}}}'.format(tag['href'], tag.get_text())

    # Preserve paragraphs
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text()
        text = replace_unicode_latex(text)
        paragraphs.append(text)

    # Join paragraphs with double line breaks (LaTeX paragraph break)
    latex_text = ''.join(paragraphs)

    return latex_text


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    latex = html_to_latex(html)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex)

    print(f"Converted LaTeX written to {output_file}")
