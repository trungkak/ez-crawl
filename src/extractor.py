from bs4 import BeautifulSoup

class Extractor(object):
    """
    Extract data from HtmlElement
    """
    def __init__(self, node):
        """
        :param node: lxml HtmlElement object
        """
