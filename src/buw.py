from lxml import etree
import lxml.html
from utils import *
import urllib.request, urllib.parse, urllib.error
from lxml.html.clean import Cleaner


class BUWrapper(object):

    def __init__(self, url):
        self.url = url

        self.root = self.construct_tree()
        self.tree = etree.ElementTree(self.root)

        self.leaf_nodes = []
        get_all_leaf_nodes(self.root, self.leaf_nodes)

    def construct_tree(self):
        doc = self.get_data()
        root = lxml.html.fromstring(doc)
        return root

    def items_removal(self):
        paths = [self.get_simplified_path(node) for node in self.leaf_nodes]
        items = [node for node in self.leaf_nodes
                 if paths.count(self.get_simplified_path(node)) >= 3]
        return items

    def get_data(self):
        page = urllib.request.urlopen(self.url)
        html_body = page.read()
        cleaner = Cleaner(javascript=True, scripts=True, style=True, kill_tags=['a'])
        doc = cleaner.clean_html(html_body)
        return doc

    def record_finder(self):
        pass

    def record_removal(self):
        pass

    def region_finder(self):
        pass

    def region_removal(self):
        pass

    def get_simplified_path(self, node):
        return re.sub(pattern, '', self.tree.getpath(node))

if __name__ == '__main__':
    wrapper = BUWrapper('https://stackoverflow.com/questions/29567684/lxml-get-all-leaf-nodes')
    items = wrapper.items_removal()
    print(items)