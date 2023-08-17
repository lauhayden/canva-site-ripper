# Canva Site Ripper

A tool to download and clean a Canva site for self-hosting.

When pointed at an existing freely hosted Canva site, this tool will download the HTML, remove all javascript and link redirection, then download all the auxiliary files (images, fonts, etc) and write them all to a single folder to be copied to a self-hosted web server.

# Development

## Tools used:

* Packaging: [Poetry](https://python-poetry.org/)
* Formatter: [Black](https://github.com/psf/black)
	* Run using `poetry run black src`
* Linter: [Pylint](https://pylint.pycqa.org/en/latest/)
	* Run using `poetry run pylint src`
* Type checking: [mypy](https://mypy.readthedocs.io/en/stable/index.html)
    * Run using `poetry run mypy src`
