from bs4 import BeautifulSoup
from lxml.etree import tostring
import lxml.html
from src.parser import Parser


class Extractor(object):
    """
    Extract data from HtmlElement
    Data includes:
        - Link
        - Author
        - Title
        - Text/Description
        - Price
        - Image
        - Date time
        - Rating
        - Comments
    """
    def __init__(self, node, type='a'):
        """
        doc: html source
        type: 'a' => article; 'c' => comment
        """
        self.type = type
        self.root = node

    def get_title_for_article(self):
        """Fetch the article title and analyze it

        Assumptions:
        - title tag is the most reliable (inherited from Goose)
        - h1, if properly detected, is the best (visible to users)
        - og:title and h1 can help improve the title extraction
        - python == is too strict, often we need to compare filtered
          versions, i.e. lowercase and ignoring special chars

        Explicit rules:
        1. title == h1, no need to split
        2. h1 similar to og:title, use h1
        3. title contains h1, title contains og:title, len(h1) > len(og:title), use h1
        4. title starts with og:title, use og:title
        5. use title, after splitting
        """
        title = ''
        text_title = Parser.find_elements_by_tag(self.root, 'title')[0].text

        h1s = Parser.find_elements_by_tag(self.root, 'h1') or []
        h1s_text = Parser.rejoin_group_text([h1.text for h1 in h1s])
        if h1s_text:
            h1s_text.sort(key=len, reverse=True)
            h1_title = h1s_text[0]

            if len(h1_title) <= 5:
                h1_title = ''

        fb_title = (

        )