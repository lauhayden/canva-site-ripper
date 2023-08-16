import argparse
import pathlib
import urllib.parse

import requests

from canva_site_ripper import clean

def parse_args():
    parser = argparse.ArgumentParser("canva-site-ripper", description="Tool for ripping and cleaning Canva websites")
    parser.add_argument("canva_url")
    parser.add_argument("new_url")
    return parser.parse_args()

def main():
    args = parse_args()
    response = requests.get(args.canva_url)
    cleaned_html, to_download = clean.clean(response.text, args.canva_url, args.new_url)

    parsed_canva_url = urllib.parse.urlparse(args.canva_url)
    downloaded = {}
    for file_to_download in to_download:
        download_url = urllib.parse.urlunparse(parsed_canva_url._replace(path=file_to_download))
        response = requests.get(download_url)
        downloaded[file_to_download] = response.content

    basedir = pathlib.Path("cleaned_website")
    basedir.mkdir(exist_ok=True)
    with (basedir / "index.html").open("w") as index_file:
        index_file.write(cleaned_html)
    for download_pathstr, downloaded_bin in downloaded.items():
        save_path = basedir / pathlib.Path(download_pathstr)
        save_path.parent.mkdir(exist_ok=True)
        with save_path.open("wb") as save_file: # TODO: make path fragment os-agnostic
            save_file.write(downloaded_bin)

if __name__ == "__main__":
    main()