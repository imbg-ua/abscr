# ABSCR library
A python library for cell recognition.
# Work in progress . . .

## Omero

- Download lib from https://github.com/imbg-ua/abscr
- Unzip 
- Make sure that name of the lib directory is `abscr`, not `abscr-main`
- `cd abscr`
- `conda env create -n cenv --file environment.yml` 

(maybe you need to replace `prefix:` in the .yml file with your path)

- `conda install conda-build`
- `conda develop .`

Bingo!
