import pprint
import re
import urllib.parse

from bs4 import BeautifulSoup


HTML = "Website.html"
HTML_CLEAN = "Website_cleaned.html"
CANVA_URL = ""
NEW_URL = ""

def clean(html, orig_url, new_url):
    soup = BeautifulSoup(html, "html.parser")
        
    # remove all script tags
    for script_tag in soup.find_all("script"):
        script_tag.decompose()
        
    # unmangle links
    for a_tag in soup.find_all("a"):
        query = urllib.parse.urlparse(a_tag["href"]).query
        real_link = urllib.parse.parse_qs(query)["link"]
        a_tag["href"] = real_link

    to_download = set()

    # extract images for download
    # img tags
    for img_tag in soup.find_all("img"):
        to_download.add(img_tag["src"])
    # favicons
    for link_tag in soup.find_all("link"):
        to_download.add(link_tag["href"])
    # cover image
    for meta_tag in soup.find_all("meta", property="og:image"):
        to_download.add(meta_tag["content"])
        
    # extract fonts for download
    for style_tag in soup.find_all("style"):
        stylesheet = style_tag.string
        # no easy way to parse the CSS :(
        # we'll just match via regex...
        for match in re.finditer("src: url\(([0-9a-z/\.]*)\);", stylesheet):
            to_download.add(match.group(1))

    # write result to string...
    string_soup = soup.prettify()

    # replace mentions of the test site...
    orig_domain = urllib.parse.urlparse(orig_url).netloc
    new_domain = urllib.parse.urlparse(new_url).netloc
    string_soup = string_soup.replace(orig_domain, new_domain)

    return string_soup, to_download
