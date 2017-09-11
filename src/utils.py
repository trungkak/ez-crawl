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


def get_record_link(node, prefix):
    a_tags = node.cssselect('a')
    if a_tags == None or len(a_tags) == 0:
        return '#'
    # if len(a_tags) == 1: # if there's just one url, returns url
    #     url = a_tags[0].get('href')
    #     return prefix + url if not url.startswith(prefix) else url
    # url_mapper = Counter()
    # for tag in a_tags:
    #     url = tag.get('href')
    #     if not url.startswith(prefix): # Internal url
    #         return prefix + url
    #     url_mapper[url] = len(Parser.get_text(tag))
    #
    # return url_mapper.most_common(1)[0][0] # Choose url with longest text
    url = a_tags[0].get('href')
    i = 1
    while url == "#" and i < len(a_tags):
        url = a_tags[i].get('href')
        i += 1
    if url == None or len(url) == 0:
        return '#'
    return prefix + url if not url.startswith(prefix) else url

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

    record_html = """
    <ul>
    <li itemscope="" itemtype="http://schema.org/Product" class="_10fX327FTBhXxwannc1Gp_">
    <a itemprop="url" class="_2-QpDA4ooHCnxpPjIDiUYD" href="/quan-binh-tan/mua-ban-nha-dat/nha-ngay-tt-tan-tao-a-38434359.htm">
    <div class="yfFxjKOyB3Fo2OkEau-wW">
    <img itemprop="image" alt="Nhà   ngay TT Tân Tạo A." class="_2QyIW9LqRbk7pxfkpTpSI6 lazyloaded" src="https://static.chotot.com.vn/mob_thumbs_app/17/1733888557.jpg">
    </div>
    <div class="_15oCrCDHNpc124ULZtp53I">
    <h3 itemprop="name" class="Gw4t5HfxzKaRjRHV9AVas">
    <!-- react-text: 224 --><!-- /react-text --><!-- react-text: 225 -->Nhà   ngay TT Tân Tạo A.<!-- /react-text --></h3>
    <div class="_1h1BByQ1mTum4oTxnd2Mb7" itemprop="offers" itemscope="" itemtype="http://schema.org/Offer"><span itemprop="price" content="1280000000" class="rbUN6Vaz5gMZ1qei6Mbrq"><!-- react-text: 228 -->1.280.000.000 đ<!-- /react-text --><!-- react-text: 229 --><!-- /react-text --></span></div></div><!-- react-text: 230 --><!-- /react-text --></a><div class="_3wMagatP7dhqM755AzyuqO"><span class="XXGpZ-FP2JDUEL80ZK7ZE"><!-- react-text: 233 -->hôm nay 10:22<!-- /react-text --><span class="hidden-xxs"><!-- react-text: 235 --> <!-- /react-text --><!-- react-text: 236 -->| Quận Bình Tân<!-- /react-text --></span></span><span class="_3F7ZRFISLZKL0eTzUD5aNP pull-right"><span title="Quốc Huy"><img class="_2Iqho-pdncc-NrQBTAGBLf pull-right img-circle " src="https://static.chotot.com.vn/imaginary/78ad5a8ba849961e00c00e823b84934a2759a252/profile_avatar/60d1f1e370ecd54982edf78b4a4d3150813d31d6/thumbnail?width=32" alt="private"><span class="_1MOBvRCbVZ58X7LdLV3Mi R6EON5H9wxUv5eo_Wv0Ep pull-right">Quốc Huy</span><div class="clear"></div></span></span></div></li>
    </ul>
    """
    # root = etree.fromstring(html_str)
    # tree = etree.ElementTree(root)
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