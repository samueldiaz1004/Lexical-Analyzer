# Lexical Analyser

Lexical Scanner for the C minus (C--) programming language.

Take a look at the `C-- Language Lexical Specification.pdf` and `Lexical analyzer - Written Report.pdf`.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libraries.

```bash
pip install -r requirements.txt
```

## Usage
Run scanner and check outputs at the `./output` folder.
```bash
python scanner.py
```
If you wish to change the input file contents you can go to `./input/source.txt` and write you own C-- code.

## Tests
* Test case 0
    * All tokens are accepted by the scanner.
* Test case 1
    * A float number ended with a '.' instead of a digit.
* Test case 2
    * Comment (/\* ... \*/) was not properly closed.
* Test case 3
    * String (" ... ") was not properly closed.
* Test case 4
    * '!' was written but never followed by a '='.
* Test case 5
    * A token contained a character outside of the English alphabet.


## License

[MIT](https://choosealicense.com/licenses/mit/)