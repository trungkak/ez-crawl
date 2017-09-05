from bs4 import BeautifulSoup
from lxml.etree import tostring
import lxml.html

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
    def __init__(self, doc, type='a'):
        """
        doc: html source
        type: 'a' => article; 'c' => comment
        """
        self.type = type
        self.doc = doc
        self.parser = lxml.html.fromstring(self.doc)

    def parse(self):
        soup = BeautifulSoup(tostring(self.doc))

    def get_title_for_article(self):
        """
        Step1: find title element, if title is found: return title
        Step2: find all h1 tag
        """
        title = ''
        title_elem = self.parser.find('.//title').text
        if title_elem is None or title_elem == '':
            return title