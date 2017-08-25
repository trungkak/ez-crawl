from lxml.html.clean import Cleaner


def clean_doc(doc):
    cleaner = Cleaner() # http://lxml.de/api/lxml.html.clean.Cleaner-class.html
    try:
        cleaner.clean_html(doc)
    except:
        raise 'Error cleaning html'
