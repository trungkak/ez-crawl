from lxml import etree
import lxml.html
from src.utils import *
from lxml.html.clean import Cleaner
from collections import defaultdict
from collections import Counter
from urllib.parse import urlsplit
import time
from fake_useragent import UserAgent
import random
import requests


class BUWrapper(object):

    def __init__(self, url):
        self.url = url
        self.prefix = self.find_prefix()

        self.root = self.construct_tree()
        self.tree = etree.ElementTree(self.root)

        self.leaf_nodes = []
        get_all_leaf_nodes(self.root, self.leaf_nodes)

    def find_prefix(self):
        prefix = "{0.scheme}://{0.netloc}".format(urlsplit(self.url))
        return prefix

    def construct_tree(self):
        doc = self.get_data()
        root = lxml.html.fromstring(doc)
        return root

    def construct_items(self):
        paths = [self.get_simplified_path(node) for node in self.leaf_nodes]
        items = [node for node in self.leaf_nodes
                 if paths.count(self.get_simplified_path(node)) >= 5]
        return items

    def group_by_path(self, node_list):
        """
        :param node_list: list of HtmlElement nodes
        :return: dict with key be simple path of nodes, value be list of node with the same simple path
        """
        grp = defaultdict(list)
        for node in node_list:
            key = self.get_simplified_path(node)
            grp[key].append(node)
        return grp

    def group_by_parent_node(self, node_list):
        grp = defaultdict(list)
        for node in node_list:
            key = find_direct_parent(node)
            grp[key].append(node)
        return grp

    def find_region_candidates(self):
        records = self.get_data_records()
        grp = self.group_by_parent_node(records)
        return grp

    def get_data(self):

        html_body = self._by_pass_get_html(self.url)

        cleaner = Cleaner()
        cleaner.comments = True
        doc = cleaner.clean_html(html_body)
        return doc

    def _by_pass_get_html(self, url):
        """ In case you are blocked """

        ua = UserAgent()
        header = {'User-Agent': str(ua.chrome)}
        print(header)

        time.sleep(0.5 * random.random())
        r = requests.get(url, headers=header)
        page_html = r.content
        return page_html

    def get_simplified_path(self, node):
        return re.sub(pattern, '', self.tree.getpath(node))

    def find_record_candidates(self):
        items = self.construct_items()
        grp_items = self.group_by_path(items)
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
                   paths.count(self.get_simplified_path(record)) >= 5]

        return records

    def go_next(self):
        symbol_next = ['»']
        pattern_next = ".*[Nn](ex|x)t.*"

        # Search with class
        xpath_class = "//*[re:test(@class, '%s')]" % pattern_next
        class_paths = self.tree.xpath(xpath_class,
                                      namespaces={'re': "http://exslt.org/regular-expressions"})
        return class_paths[-1]

    def get_main_content(self):
        """
        Idea:
        1. Find the largest text block from each record in each region
        2. Measure entropy for each region based on largest text blocks size
        3. Main content is the block with maximum entropy
        """
        grp_regions = self.find_region_candidates()
        grp_regions = {region:grp_regions[region] for region in grp_regions if not is_static(region)}

        # for region in list(grp_regions.keys()):
        #     print('---------')
        #     print(etree.tostring(region))
        #     print('---------')

        d_entropy = Counter()
        for path in list(grp_regions.keys()):
            region = grp_regions[path]
            text_lens = []
            for record in region:
                text_lens.append(len(get_largest_text(record)))  # Step 1
            entropy = compute_entropy(text_lens)  # Step 2
            d_entropy[path] = entropy

        main_region_paths = d_entropy.most_common(2)    # Step 3: Choose 2 richest path

        final_path1 = max(main_region_paths, key=lambda elem: len(elem[0]))[0]

        final_path2 = d_entropy.most_common(1)[0][0]

        if len(grp_regions[final_path1]) > len(grp_regions[final_path2]):
            return grp_regions[final_path1]
        else:
            return grp_regions[final_path2]


if __name__ == '__main__':
    url = 'https://tiki.vn/day-sac-day-cap/c1823?src=mega-menu'
    wrapper = BUWrapper(url)
    main_content = wrapper.get_main_content()
    # record_urls = list(set([Parser.get_text(record) for record in main_content]))
    for record in main_content:
        print(list(record.itertext()))
    print(len(main_content))