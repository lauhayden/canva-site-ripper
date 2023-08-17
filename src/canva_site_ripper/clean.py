"""Parse and modify the HTML"""

import re
from typing import Set, TextIO, Tuple
import urllib.parse

from bs4 import BeautifulSoup


HTML = "Website.html"
HTML_CLEAN = "Website_cleaned.html"
CANVA_URL = ""
NEW_URL = ""


def path_only(url: str) -> str:
    """Return only the path portion of a URL without a leading /

    Args:
        url: unparsed URL string

    Returns:
        path portion of the URL
    """
    return urllib.parse.urlparse(url).path.lstrip("/")


def clean(
    html: TextIO, orig_url: urllib.parse.ParseResult, new_url: urllib.parse.ParseResult
) -> Tuple[str, Set[str]]:
    """Parsing and modifying logic.

    Args:
        html: text representing the HTML file
        orig_url: the original canva site URL, in parsed form
        new_url: the url that the website will be hosted at, in parsed form

    Returns:
        strsoup: string representation of the modified HTML
        to_download: a set of paths relative to the original URL to download auxiliary files from
            (eg. images, fonts)
    """
    soup = BeautifulSoup(html, "html.parser")

    # remove all script tags
    for script_tag in soup.find_all("script"):
        script_tag.decompose()

    # unmangle links
    # Canva likes to redirect all links, so we extract the real link from the query parameters
    # and put it back into the tag
    for a_tag in soup.find_all("a"):
        query = urllib.parse.urlparse(a_tag["href"]).query
        real_link = urllib.parse.parse_qs(query)["link"]
        a_tag["href"] = real_link

    to_download = set()

    # extract images for download
    # img tags
    for img_tag in soup.find_all("img"):
        to_download.add(path_only(img_tag["src"]))
        if "srcset" in img_tag.attrs:
            # https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset
            for srcset_candidate in img_tag["srcset"].split(","):
                to_download.add(path_only(srcset_candidate.strip().split(" ")[0]))
    # favicons
    for link_tag in soup.find_all("link"):
        to_download.add(path_only(link_tag["href"]))
    # cover image
    for meta_tag in soup.find_all("meta", property="og:image"):
        to_download.add(path_only(meta_tag["content"]))

    # extract fonts for download
    for style_tag in soup.find_all("style"):
        stylesheet = style_tag.string
        # no easy way to parse the CSS :(
        # we'll just match via regex...
        # we're looking for stuff like "src: url(fonts/7723ea9f98a16ef490f29d77b7188065.woff2);"
        for match in re.finditer(r"src: url\(([0-9a-z/\.]*)\);", stylesheet):
            to_download.add(path_only(match.group(1)))

    # write result to string
    # using prettify() messes up by adding in additional newlines in the text
    string_soup = str(soup)

    # replace mentions of the test site
    orig_domain = orig_url.netloc
    new_domain = new_url.netloc
    # using naive string replace works because the domain match should be exact
    # still, a bit risky. may want to do something smarter later
    string_soup = string_soup.replace(orig_domain, new_domain)

    return string_soup, to_download
