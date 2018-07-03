import pywikibot, string, sys
from pywikibot import pagegenerators
from pywikibot import textlib
site = pywikibot.Site()

strings = ["BravelyD"]

def print_to_wiki(pages):
    log = pywikibot.Page(site, 'User:Intangir Bot/Logs/String Search')
    l = 'Updated ~~~~~\n\n'
    for page in pages:
        l += '#[[' + page + ']]: ' + str(pages[page]) + '\n'
    log.text = l
    log.save(u'Logging class search')

def string_search(page):
    p = ''
    for s in strings:
        if s in page:
            p += s + ", "
    if len(p) > 0:
        # print(p)
        return p
    return False

def main(*args):
    pages = {}
    namescapes = {0, 4, 8, 10, 12, 828}
    for ns in namescapes:
        gen = site.allpages(start="List",namespace=ns)
        for page in gen:
            # print(page.title())
            clssea = string_search(page.text)
            if clssea:
                pages[page] = clssea
    print_to_wiki(pages)

if __name__ == "__main__":
    main()
