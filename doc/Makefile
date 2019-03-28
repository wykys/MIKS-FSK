# wykys LaTeX Makefile

LATEX = pdflatex
FLAGS = -halt-on-error -interaction=nonstopmode

NAME = doc
PDF_READER = zathura

.PHONY: all

# make document
all:
	@$(LATEX) $(FLAGS) $(NAME).tex
	@$(LATEX) $(FLAGS) $(NAME).tex
	@echo -n "\033[0;31mNormostran: \033[0m"
	@echo "scale=2; `detex -n *.tex | wc -c`/1800;" | bc
	@#ps -a | grep $(PDF_READER) || nohup $(PDF_READER) $(NAME).pdf