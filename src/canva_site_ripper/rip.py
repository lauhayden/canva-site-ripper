import argparse
import os
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

    os.makedirs("cleaned_website", exist_ok=True)
    with open(os.path.join("cleaned_website", "index.html"), "w") as index_file:
        index_file.write(cleaned_html)
    for path, downloaded_bin in downloaded.items():
        with open(os.path.join("cleaned_website", path), "wb") as path_file: # TODO: make path fragment os-agnostic
            path_file.write(downloaded_bin)

if __name__ == "__main__":
    main()