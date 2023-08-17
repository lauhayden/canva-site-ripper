import argparse
import pathlib
import urllib.parse

import requests

from canva_site_ripper import clean

def parse_args():
    parser = argparse.ArgumentParser("canva-site-ripper", description="Tool for ripping and cleaning Canva websites")
    parser.add_argument("canva_url", help="URL of the Canva site.", type=urllib.parse.urlparse)
    parser.add_argument("new_url", help="URL that the site will be hosted on.", type=urllib.parse.urlparse)
    parser.add_argument("-f", "--file", help="Use this HTML file instead of download directly from Canva.", type=argparse.FileType("r"))
    parser.add_argument("-r", "--no-robots", action="store_true", help="Add a robots.txt disallowing all crawlers to the output")
    return parser.parse_args()

def main():
    # TODO: use persistent pool with requests?
    args = parse_args()
    if args.file:
        html = args.file
    else:
        html = requests.get(urllib.parse.urlunparse(args.canva_url)).text
    cleaned_html, to_download = clean.clean(html, args.canva_url, args.new_url)

    # TODO: search for "canva" in the cleaned HTML

    downloaded = {}
    for file_to_download in to_download:
        download_url = urllib.parse.urlunparse(args.canva_url._replace(path=file_to_download))
        response = requests.get(download_url)
        downloaded[file_to_download] = response.content

    # TODO: delete existing
    basedir = pathlib.Path("cleaned_website")
    basedir.mkdir(exist_ok=True)
    with (basedir / "index.html").open("w") as index_file:
        index_file.write(cleaned_html)
    for download_pathstr, downloaded_bin in downloaded.items():
        save_path = basedir / pathlib.Path(download_pathstr)
        save_path.parent.mkdir(exist_ok=True)
        with save_path.open("wb") as save_file:
            save_file.write(downloaded_bin)

    if args.no_robots:
        with (basedir / "robots.txt").open("w") as robots_file:
            robots_file.write("User-agent: *\nDisallow: /\n")

if __name__ == "__main__":
    main()