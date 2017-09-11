from bs4 import UnicodeDammit
from lxml.etree import tostring, fromstring

class Parser(object):

    @classmethod
    def decode_html(cls, html):
        """
        Example from http://lxml.de/elementsoup.html
        """
        converted = UnicodeDammit(html)
        if not converted.unicode_markup:
            raise UnicodeDecodeError("Failed to detect encoding,\
             tried [%s]",', '.join(converted.tried_encodings))
        return converted.unicode_markup

    @classmethod
    def fromstring(cls, html_str):
        return fromstring(cls.decode_html(html_str))

    @classmethod
    def tostring(cls, node):
        return tostring(node)

    @classmethod
    def find_element_by_id(cls, node, id):
        selector = '//*[@id="%s"]' % id
        elems = node.xpath(selector)
        if elems:
            return elems[0]
        return None

    @classmethod
    def find_elements_by_tag(cls, node, tag, attr=None):
        if attr:
            selector = '//%s[@%s="%s"]' % (tag, list(attr.items())[0][0], list(attr.items())[0][1])
        else:
            selector = '//%s' % tag
        elems = node.xpath(selector)
        if elems:
            return elems
        return []

    @classmethod
    def get_text(cls, node):
        return node.text_content()

    @classmethod
    def stringify_node(cls, node):
        return node.text

if __name__ == '__main__':
    html = """
    <div data-hook="review-collapsed" aria-expanded="false" class="a-expander-content a-expander-partial-collapse-content">Perfect shoe, super comfortable and high quality. I wish I could post photos they come with an authentic Jordan black and gold box, 23 shoe paper, the shoes themselves and shoe trees. Overall they are perfect shoes for me on and off cort I went with the black, gym red, and white color way, and might I say they look stunning. With all the shoes pros there is just 1 con, no receipt. That isn't a huge deal but if you resale after wearing, that might be a bit if an issue for you. I can aslo add these shoes are %100 authentic. If your looking for a good looking shoe for a lower price than $100 you can't beat the Jordan 1 mid!</div>
    """
    root = Parser.fromstring(html)
    print(Parser.stringify_node(root))