"""Main ripping logic"""

import argparse
import pathlib
import shutil
import urllib.parse

import requests

from canva_site_ripper import clean


def dir_path(argstr: str) -> pathlib.Path:
    """Parse, delete recursively, and remake the output dir.

    Args:
        argstr: raw input from the argument

    Returns:
        the output dir path
    """
    try:
        path = pathlib.Path(argstr)
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass
    except Exception as err:
        # transform error into ArgumentTypeError for argparse to print appropriate info
        raise argparse.ArgumentTypeError("can't delete existing directory: " + str(err)) from err
    try:
        path.mkdir()
    except Exception as err:
        raise argparse.ArgumentTypeError("can't create output directory: " + str(err)) from err
    return path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        parsed arguments
    """
    parser = argparse.ArgumentParser(
        "canva-site-ripper", description="Tool for ripping and cleaning Canva websites"
    )
    parser.add_argument("canva_url", help="URL of the Canva site.", type=urllib.parse.urlparse)
    parser.add_argument(
        "new_url", help="URL that the site will be hosted on.", type=urllib.parse.urlparse
    )
    parser.add_argument(
        "output_dir",
        help="Directory to save the website files. Existing files will be deleted.",
        type=dir_path,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Use this HTML file instead of downloading from Canva as the index.html.",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "-r",
        "--no-robots",
        action="store_true",
        help="Add a robots.txt disallowing all crawlers to the output",
    )
    return parser.parse_args()


def main() -> None:
    """Main function."""
    with requests.Session() as session:
        args = parse_args()
        if args.file:
            html = args.file
        else:
            html = session.get(urllib.parse.urlunparse(args.canva_url)).text
        cleaned_html, to_download = clean.clean(html, args.canva_url, args.new_url)

        if "canva" in cleaned_html.lower():
            print("Warning: string 'canva' found in cleaned HTML")

        # download all auxiliary files
        responses = {}
        for file_to_download in to_download:
            download_url = urllib.parse.urlunparse(args.canva_url._replace(path=file_to_download))
            response = session.get(download_url)
            responses[file_to_download] = response

        # write everything to disk
        with (args.output_dir / "index.html").open("w") as index_file:
            index_file.write(cleaned_html)
        for download_pathstr, response in responses.items():
            save_path = args.output_dir / pathlib.Path(download_pathstr)
            save_path.parent.mkdir(exist_ok=True)
            with save_path.open("wb") as save_file:
                save_file.write(response.content)

    if args.no_robots:
        with (args.output_dir / "robots.txt").open("w") as robots_file:
            robots_file.write("User-agent: *\nDisallow: /\n")


if __name__ == "__main__":
    main()
