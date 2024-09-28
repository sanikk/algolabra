# User manual

## Installation

Project dependencies are installed with poetry:

```bash
poetry install
```

## Running
```bash
poetry run invoke start
```
## Tests
```bash
poetry run invoke test
```
## Coverage
Generate report
```bash
poetry run invoke coverage-report
```
Output report as html into htmlcov directory, see index.html
```bash
coverage html
```
Output report as text on the command line
```bash
coverage report
```