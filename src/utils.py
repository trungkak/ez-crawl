from lxml.html.clean import Cleaner
from lxml import etree
import re

# Constants
pattern = r'\[[^\]]*\]'


def get_all_leaf_nodes(node, leaf_nodes=[]):
    if node.getchildren():
        for child in node:
            get_all_leaf_nodes(child,leaf_nodes)
    else:
        leaf_nodes.append(node)


if __name__ == '__main__':
    html_str = """
    <html>
        <head>
            <title>Test title</title>
        </head>
        <body>
            <div><span>Here</span>
                <div>
                    <div>
                        <span>Here</span>
                        <span>There</span>
                    </div>
                    <div>
                        <span>Here</span>
                    </div>
                </div>
            </div>
        </body>
    </html>"""
    root = etree.fromstring(html_str)
    tree = etree.ElementTree(root)
    leaf_nodes = []
    get_all_leaf_nodes(root, leaf_nodes)
    for node in leaf_nodes:
        # print(tree.getpath(node))
        print(get_simplified_path(node, tree))