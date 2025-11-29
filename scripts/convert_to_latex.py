import re
import sys
from bs4 import BeautifulSoup

# Mapping Unicode to LaTeX (without quotes — handled by csquotes)
UNICODE_LATEX = {
    # punctuation and ligatures
    '…': r'\ldots',
    '“‘': r'``\hspace{0pt}`',    '’”': r"'\hspace{0pt}''",
    '‘“': r'`\hspace{0pt}``',    '”’': r"''\hspace{0pt}'",
    '“': '``',      '”': "''",
    '‘': '`',       '’': "'",
    '–': '--',      '—': '---',
    'ç': r'\c{c}',  'Ç': r'\c{C}',
    'ñ': r'\~n',    'Ñ': r'\~N',
    'œ': r'\oe ',   'Œ': r'\OE ',

    # A vowels
    'à': r'\`a',    'À': r'\`A',
    'á': r"\'a",    'Á': r"\'A",
    'â': r'\^a',    'Â': r'\^A',
    'ä': r'\"a',    'Ä': r'\"A',
    'ã': r'\~a',    'Ã': r'\~A',
    'å': r'\r a',   'Å': r'\r A',
    'ā': r'\=a',    'Ā': r'\=A',
    'ă': r'\u a',   'Ă': r'\u A',
    'ą': r'\k a',   'Ą': r'\k A',

    # E vowels
    'è': r'\`e',    'È': r'\`E',
    'é': r"\'e",    'É': r"\'E",
    'ê': r'\^e',    'Ê': r'\^E',
    'ë': r'\"e',    'Ë': r'\"E',
    'ē': r'\=e',    'Ē': r'\=E',
    'ĕ': r'\u e',   'Ĕ': r'\u E',
    'ė': r'\.e',    'Ė': r'\.E',
    'ę': r'\k e',   'Ę': r'\k E',

    # I vowels
    'ì': r'\`i',    'Ì': r'\`I',
    'í': r"\'i",    'Í': r"\'I",
    'î': r'\^i',    'Î': r'\^I',
    'ï': r'\"i',    'Ï': r'\"I',
    'ī': r'\=i',    'Ī': r'\=I',
    'ĭ': r'\u i',   'Ĭ': r'\u I',
    'į': r'\k i',   'Į': r'\k I',
    'ı': r'{\i}',   # dotless i

    # O vowels
    'ò': r'\`o',    'Ò': r'\`O',
    'ó': r"\'o",    'Ó': r"\'O",
    'ô': r'\^o',    'Ô': r'\^O',
    'ö': r'\"o',    'Ö': r'\"O',
    'õ': r'\~o',    'Õ': r'\~O',
    'ō': r'\=o',    'Ō': r'\=O',
    'ŏ': r'\u o',   'Ŏ': r'\u O',
    'ő': r'\H o',   'Ő': r'\H O',  # double acute

    # U vowels
    'ù': r'\`u',    'Ù': r'\`U',
    'ú': r"\'u",    'Ú': r"\'U",
    'û': r'\^u',    'Û': r'\^U',
    'ü': r'\"u',    'Ü': r'\"U',
    'ū': r'\=u',    'Ū': r'\=U',
    'ŭ': r'\u u',   'Ŭ': r'\u U',
    'ů': r'\r u',   'Ů': r'\r U',
    'ű': r'\H u',   'Ű': r'\H U',
    'ų': r'\k u',   'Ų': r'\k U',

    # Y vowels (sometimes accented in foreign languages)
    'ý': r"\'y",    'Ý': r"\'Y",
    'ÿ': r'\"y',    'Ÿ': r'\"Y',
    'ȳ': r'\=y',    'Ȳ': r'\=Y',
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
        format_text = f.read()

    if input_file.endswith(".html"):
        latex = html_to_latex(format_text)
    else:
        latex = replace_unicode_latex(format_text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex)

    print(f"Converted LaTeX written to {output_file}")
