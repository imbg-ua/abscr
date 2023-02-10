# ABSCR library
A python library for cell recognition.
# Work in progress . . .

## Install

- Download library from https://github.com/imbg-ua/abscr
- Unzip 
- Make sure that name of the lib directory is `abscr`, not `abscr-main`
- `cd abscr`
- `conda env create -n cenv --file environment.yml` 

(maybe you need to replace `prefix:` in the .yml file with your path or just comment this line)

- `conda install conda-build`
- `conda develop .`

Bingo!

## GPU support with pure conda

- Use "environment_explicit.yml" file to create conda environment
- `conda env create -n cenv --file environment_explicit.yml`
- `conda develop .`
- `python -m ipykernel install --user --name=cenv`
