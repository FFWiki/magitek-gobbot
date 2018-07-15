import pywikibot, random, string, sys
from pywikibot import (
    pagegenerators,
    textlib,
    OtherPageSaveError
)

SITE = pywikibot.Site()

def kill(page):
    page.delete(reason="Deprecated FFXIV icon.", prompt=False)

def main(*args):
    gen = pagegenerators.AllpagesPageGenerator(start="Icon-ffxiv-", namespace=6)
    for page in gen:
        if "-ffxiv-" not in page.title():
            break
        kill(page)

if __name__ == "__main__":
    main()
