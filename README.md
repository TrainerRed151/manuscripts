# Book Formatting Tools and LaTeX Sources

This repository contains the scripts, LaTeX sources, and supporting materials used to format books into clean, reusable text blocks. The project is designed for preparing publication-ready layouts, generating print-ready PDFs, and standardizing formatting across multiple manuscripts.

## Contents

* **`scripts/`** -- Python, Bash, and other scripts used for preprocessing text from HTML for LaTeX and compiling LaTeX files into signatures.
* **`books/`** -- Source text for individual books (original manuscript text, public domain text, or third-party text included with permission).
* **`cad_designs/`** -- OpenSCAD and STL files for bookbinding tools (see LICENSE in directories where applicable).
* **`requirments.txt`** -- Python required packages.
* **`LICENSE`** -- Licensing terms for the materials in this repository.

## Purpose

This project provides a reproducible pipeline for converting raw text into polished, typeset text blocks for hard-back binding.

## How It Works

1. **Prepare the text**
   Scripts in `scripts/` clean and normalize the manuscript (e.g., whitespace fixes, smart punctuation, structural tagging).


2. **Build the book**
   Use the provided scripts or compile manually with `pdflatex` and `pdfjam`.

## Requirements

* Docker installed on machine
* Python 3.x for preprocessing scripts
  - Install required Python packages:
  ```shell
  pip install -r requirements.txt
  ```

## Licensing

All original materials in this repository are covered by the terms in the `LICENSE` file.
Some materials may be:

* third-party copyrighted content included with permission, or
* public-domain text included for reference.

See the `LICENSE` file for full details.
