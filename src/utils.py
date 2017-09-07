from lxml.html.clean import Cleaner
from lxml import etree
import re
from math import log

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
    :param list_children:
    :return: How many children of parent node is in list children
    """
    descendants = ancestor.findall('.//')  # find all descendants of a node
    return len(list(set(descendants) & set(list_node)))


def find_all_ancestors(node):
    return node.iterancestors()


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

    leaf_nodes = []
    get_all_leaf_nodes(root, leaf_nodes)
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