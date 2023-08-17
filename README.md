# Canva Site Ripper

A tool to download and clean a Canva site for self-hosting.

When pointed at an existing freely hosted Canva site, this tool will download the HTML, remove all javascript and link redirection, then download all the auxiliary files (images, fonts, etc) and write them all to a single folder to be copied to a self-hosted web server.

## Usage

* Download and install Poetry
* Install using `poetry install`
* `poetry run canva-site-ripper --help`

```
hayden@localhost:~/Source/canva-site-ripper$ poetry run canva-site-ripper --help
usage: canva-site-ripper [-h] [-f FILE] [-r] canva_url new_url output_dir

Tool for ripping and cleaning Canva websites

positional arguments:
  canva_url             URL of the Canva site.
  new_url               URL that the site will be hosted on.
  output_dir            Directory to save the website files. Existing files will be deleted.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Use this HTML file instead of downloading from Canva as the index.html.
  -r, --no-robots       Add a robots.txt disallowing all crawlers to the output
```

# Development

## Tools used:

* Packaging: [Poetry](https://python-poetry.org/)
* Formatter: [Black](https://github.com/psf/black)
	* Run using `poetry run black src`
* Linter: [Pylint](https://pylint.pycqa.org/en/latest/)
	* Run using `poetry run pylint src`
* Type checking: [mypy](https://mypy.readthedocs.io/en/stable/index.html)
    * Run using `poetry run mypy src`
