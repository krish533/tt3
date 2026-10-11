.PHONY: reproduce paper test sync
reproduce:
	python3 code/replicate.py
paper:
	python3 code/replicate.py --pdf
test:
	python3 -m unittest discover -s tests -v
sync:
	python3 code/sync_overleaf.py
