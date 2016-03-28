name   ?= doc
outdir ?= pdf
tex = $(name).tex
pdf = $(tex:.tex=.pdf)

all: build

.PHONY: build
build:
	@mkdir -p $(outdir)
	pdflatex $(tex)
	pdflatex $(tex)
	mv $(pdf) $(outdir)/

.PHONY: clean
clean:
	rm -f *.log *.aux
	rm -f $(outdir)/$(pdf)
