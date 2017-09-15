from lxml.html.clean import Cleaner
from lxml import etree
import re
from math import log
from src.parser import Parser
from collections import Counter

# Constants
pattern = r'\[[^\]]*\]'


def get_all_leaf_nodes(node, leaf_nodes=[]):
    if node.getchildren():
        for child in node:
            get_all_leaf_nodes(child, leaf_nodes)
    else:
        leaf_nodes.append(node)


def count_descendants(ancestor, list_node):
    """
    :param ancestor:
    :param list_node:
    :return: How many children of parent node is in list children
    """
    descendants = ancestor.findall('.//')  # find all descendants of a node
    return len(list(set(descendants) & set(list_node)))


def find_all_ancestors(node):
    return node.iterancestors()


def find_direct_parent(node):
    return node.getparent()


def check_record_candidate(node, list_node):
    candidates = []
    for ancestor in find_all_ancestors(node):
        if count_descendants(ancestor,list_node) == 1 and count_descendants(ancestor.getparent(), list_node) > 1:
            candidates.append(ancestor)
    return candidates


def is_grandparent(ancestor_node, node):
    return ancestor_node in list(node.iterancestors())


def get_largest_text(node):
    if len(list(node.itertext())) == 0 or node.itertext() == None:
        return ""
    txt_lst = [re.sub(' +',' ',text) for text in list(node.itertext())]
    return max(txt_lst, key=len)


def compute_entropy(lst):
    if all(elem == 0 for elem in lst):
        return -1
    try:
        s = 1.0*sum(lst)
        lst = [(elem/s)*log(elem/s) for elem in lst]
        return -1*sum(lst)
    except:
        return -1


def get_region_size(node):
    return len(etree.tostring(node))


def get_max_dict(dct):
    max_tup = max(dct, key=lambda item: get_region_size(item))
    return max_tup


def get_record_link(node, prefix):
    a_tags = Parser.find_elements_by_tag(node, 'a')
    if a_tags is None or len(a_tags) == 0:
        return '#'
    url = a_tags[0].get('href')
    i = 1
    while url == "#" and i < len(a_tags):
        url = a_tags[i].get('href')
        i += 1
    if url is None or len(url) == 0:
        return '#'
    return prefix + url if not url.startswith(prefix) else url


def is_static(node):
    """
    Ignore elements containing static component properties
    such as: "nav", "histogram", ..
    """
    patterns_static = [".*[Nn]av.*", ".*[Hh]istogram.*"]
    node_class = node.get('class')
    if node_class:
        for pattern in patterns_static:
            if re.match(pattern, node_class):
                return True
    # children = node.getchildren() or []
    # for child in children:
    #     child_class = child.get('class')
    #     if not child_class:
    #         continue
    #     for pattern in patterns_static:
    #         if re.match(pattern, child_class):
    #             return True
    return False

def has_id(node):
    """
    Data region usually has id
    """

if __name__ == '__main__':
    html_str = """
    <html>
        <head>
            <title>Test title</title>
        </head>
        <body>
            <div><span>Here</span>
                <div>
                    <food>
                        <span>Here</span>
                        <p>There</p>
                    </food>
                    <fish>
                        <span>Here</span>
                        <p>There</p>
                    </fish>
                </div>
            </div>
        </body>
    </html>"""

    root = etree.fromstring(html_str)
    tree = etree.ElementTree(root)
    #
    # leaf_nodes = []
    # get_all_leaf_nodes(root, leaf_nodes)
    # for node in leaf_nodes:
    #     print(tree.getpath(node))

    # body = root.getchildren()[1]
    # for elem in body.findall('.//'):
    #     print(elem)

    # div = root.getchildren()[1].getchildren()[0]
    # for ancestor in find_all_ancestors(div):
    #     print(ancestor)
    # print(find_all_ancestors(div))

    # candidates = []
    # for node in leaf_nodes:
    #     candidates.extend(check_record_candidate(node, leaf_nodes))
    #
    # for candidate in candidates:
    #     print(candidate)

    # node = leaf_nodes[2]
    # print(node.getparent())
    # print(is_grandparent(root.getchildren()[0], node))

    # print(get_record_link(etree.fromstring(record_html)))