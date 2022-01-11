JUPYTER = jupyter
PYTHON3 = python3

markdown:
	$(JUPYTER) nbconvert *.ipynb --to markdown --ExtractOutputPreprocessor.enabled=False --TagRemovePreprocessor.remove_cell_tags remove
	$(PYTHON3) update_markdown.py
