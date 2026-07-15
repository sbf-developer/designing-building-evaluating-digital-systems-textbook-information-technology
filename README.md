# Designing, Building, and Evaluating Digital Systems

An introductory-to-master's-level textbook in information technology, digitalisation, and application development.

This repository contains the LaTeX source, executable examples, tests, datasets, figure scripts, book roadmap, and build instructions. The book uses Python as its primary teaching language and a small Flask/SQLite application as its recurring full-stack case.

## Build the book

Requirements:

- Python 3.11 or newer
- a LaTeX installation with `pdflatex`, `bibtex`, and the packages used in `preamble.tex`
- `make` (optional)

```bash
make pdf
```

The PDF is written to `book/information-technology-textbook.pdf`.

To build without `make`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
bibtex build/main
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
mkdir -p book
cp build/main.pdf book/information-technology-textbook.pdf
```

## Test the examples

```bash
make test
```

The web application can be run locally with:

```bash
cd examples/webapp
python -m venv .venv
. .venv/bin/activate       # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000/` in a browser. The application is deliberately small enough to understand, but includes a domain layer, persistence, validation, a JSON API, HTML rendering, tests, and security notes.

## Scope and source policy

The book map describes the intended progression through information technology, digitalisation, and application development. `coverage-matrix.csv` records how the chapters connect concepts, practical work, evidence, and prerequisites. It is an editorial planning document, not an institutional curriculum or assessment specification.

The book distinguishes established theory, empirical findings, professional conventions, teaching simplifications, and the author's synthesis. References are collected in `references.bib`.

## Contents

The manuscript is organised as a progression:

1. foundations, computational thinking, and programming;
2. algorithms, software engineering, modelling, and systems;
3. interaction design, databases, information systems, and teams;
4. research, human-centred AI, entrepreneurship, and the master's thesis.

The recurring case, CivicQueue, is a fictional public-service appointment and case-coordination system. It is used to connect requirements, domain modelling, interfaces, APIs, data, organisational change, evaluation, and research claims without treating a prototype as proof of social benefit.
