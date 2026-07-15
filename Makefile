PYTHON ?= python3
PDF := build/information-technology-textbook.pdf

.PHONY: all pdf test figures clean

all: pdf test

pdf:
	mkdir -p build
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build -auxdir=build main.tex
	cp build/main.pdf $(PDF)

test:
	$(PYTHON) -m unittest discover -s examples -p 'test_*.py' -v
	$(PYTHON) -m compileall -q examples

figures:
	$(PYTHON) figures/complexity_plot.py

clean:
	rm -rf build/*
