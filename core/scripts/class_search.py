import pywikibot, random
from pywikibot import (
    pagegenerators,
    OtherPageSaveError
)
site = pywikibot.Site()

CLASSES = ["shaded",
    "nolinkcolor",
    "selflink",
    "archive",
    "sprite-size",
    "fade",
    "grayscale",
    "invert",
    "ilspoiler",
    "flowchart",
    "board"]
NAMESPACES = [0, 4, 8, 10, 12, 828]
TOLERANCE = .005

def print_to_wiki(pages):
    log = pywikibot.Page(site, "User:Intangir Bot/Logs/Class Search")
    l = "Updated ~~~~~\n\n"
    for page in pages:
        l += "#[[" + page + "]]: " + str(pages[page]) + "\n"
    log.text = l
    log.save(u'Updating class search log')

def class_search(page):
    i = 0
    j = 0
    classes = ""
    while page.text.find("class=\"", j) != -1:
        i = page.text.find("class=\"", j)
        j = page.text.find("\"", i + 7)
        for cls in CLASSES:
            if cls in page.text[i:j]:
                classes += cls
    if classes != "":
        return classes
    return False

def random_check(page):
    if random.uniform(0, 1) < TOLERANCE:
        print(page.title() + " is now done!")

def main(*args):
    pages = {}
    for ns in NAMESPACES:
        gen = site.allpages(start="!", namespace=ns)
        for page in gen:
            classes = class_search(page)
            if classes:
                pages[page] = classes
                print(page.title() + ": " + classes)
            random_check(page)
    print_to_wiki(pages)

if __name__ == "__main__":
    main()
