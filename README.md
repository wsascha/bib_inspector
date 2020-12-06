# bib Inspector

I use this script to check my bib file for required fields specified in `reference_information.pdf`, depending on different reference types.

## Usage

```bash
bib_inspector.py [-h] [-i input.bib] [--optional [OPTIONAL]]

Inspect bib files with required fields.

optional arguments:
  -h, --help            show this help message and exit
  -i input.bib          Input .bib file
  --optional [OPTIONAL]
                        Show optional warnings
```


## Requirements

- python3
- `bibtexparser` lib (available via pip)