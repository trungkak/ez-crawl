from lxml import etree, html
from lxml.html import tostring, parse
from lxml.html.clean import Cleaner

T1 = 50  # max density region distance threshold
T2 = 20  # min region density threshold


class SD(object):
    def __init__(self, url):
        self.url = url

    def construct_tree(self):
        tree = self.collect_data()
        return tree.getroottree()

    def collect_data(self):
        raw_html = parse(self.url)
        cleaned_html = self.clean_doc(raw_html)
        doc = html.fromstring(cleaned_html)
        return doc

    def clean_doc(self, doc):
        # http://lxml.de/api/lxml.html.clean.Cleaner-class.html
        cleaner = Cleaner(
            javascript = True,
            style = True
        )
        try:
            doc = cleaner.clean_html(self.doc)
        except:
            raise 'Error cleaning html'
        return doc

    def density_validate(self):
        pass

if __name__ == '__main__':
    # url = 'https://stackoverflow.com/questions/70528/why-are-pythons-private-methods-not-actually-private'
    # sd= SD(url)
    # sd.collect_data()
    # # print(doc)
    # print(tostring(sd.clean_doc(), encoding='unicode', pretty_print=True))
    cleaner = Cleaner(javascript=True, style=True)
    # cleaner.javascript = True  # This is True because we want to activate the javascript filter
    # cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter

    url = 'http://edition.cnn.com/'
    print("WITH JAVASCRIPT & STYLES")
    print(tostring(parse(url), encoding='unicode', pretty_print=True))
    print("WITHOUT JAVASCRIPT & STYLES")
    print(tostring(cleaner.clean_html(parse(url)), encoding='unicode', pretty_print=True))