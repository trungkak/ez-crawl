from lxml import etree
import lxml.html
from src.utils import *
from lxml.html.clean import Cleaner
from collections import defaultdict
from selenium import webdriver
from pyvirtualdisplay import Display


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

    def construct_items(self):
        paths = [self.get_simplified_path(node) for node in self.leaf_nodes]
        items = [node for node in self.leaf_nodes
                 if paths.count(self.get_simplified_path(node)) >= 3]
        return items

    def group_items(self, items):
        grp = defaultdict(list)
        for item in items:
            key = self.get_simplified_path(item)
            grp[key].append(item)
        return grp

    def group_records(self, records):
        pass

    def get_data(self):
        display = Display()
        display.start()
        driver = webdriver.Firefox()
        driver.get(self.url)
        html_body = driver.page_source
        cleaner = Cleaner(javascript=True, scripts=True, style=True)
        doc = cleaner.clean_html(html_body)
        return doc

    def get_simplified_path(self, node):
        return re.sub(pattern, '', self.tree.getpath(node))

    def find_record_candidates(self):
        items = self.construct_items()
        grp_items = self.group_items(items)
        candidates = []
        for path in list(grp_items.keys()):
            for node in grp_items[path]:
                candidates.extend(check_record_candidate(node, grp_items[path]))
        return list(set(candidates))

    def get_data_records(self):
        """
        Filter out all data records that has only one data item (global) and less than 3 simplified path
        """
        items = self.construct_items()
        records = self.find_record_candidates()

        paths = [self.get_simplified_path(record) for record in records]
        records = [record for record in records
                   if count_descendants(record, items) > 1 and
                   paths.count(self.get_simplified_path(record)) >= 3]

        return records

if __name__ == '__main__':
    # wrapper = BUWrapper('https://sourceforge.net/projects/issabelpbx/reviews/?sort=created_date&stars=0#reviews-n-ratings')
    wrapper = BUWrapper('https://www.amazon.com/s/ref=a9_asi_1?rh=i%3Aaps%2Ck%3Ayeezy&keywords=yeezy&ie=UTF8&qid=1503993123')
    items = wrapper.get_data_records()
    for item in items:
        print('<<<<')
        print(etree.tostring(item, pretty_print=True))
        print('>>>>')

    print(len(items))