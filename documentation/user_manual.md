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
After starting you can choose a scenario file, like one from movingai. have the scenario file and map in the 
same location. Currently this only understands open '.' and blocked terrain from the maps.

There are a few buttons. You'll figure it out.

If the shown maps have a lot of data they take a lot of memory. You can reset
at least some of the load by choosing a different scenario before switching tabs. Also
if you switch scenarios the results disappear. Might want to take screenshot before that.

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