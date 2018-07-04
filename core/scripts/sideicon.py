import pywikibot, random, string, sys
from pywikibot import pagegenerators
from pywikibot import textlib
site = pywikibot.Site()

codenames = {
    'Final Fantasy': 'FFI',
    'Final Fantasy II': 'FFII',
    'Final Fantasy III': 'FFIII',
    'Final Fantasy IV': 'FFIV',
    'Final Fantasy V': 'FFV',
    'Final Fantasy VI': 'FFVI',
    'Final Fantasy VII': 'FFVII',
    'Final Fantasy VIII': 'FFVIII',
    'Final Fantasy IX': 'FFIX',
    'Final Fantasy X': 'FFX',
    'Final Fantasy XI': 'FFXI',
    'Final Fantasy XII': 'FFXII',
    'Final Fantasy XIII': 'FFXIII',
    'Final Fantasy XIV': 'FFXIV',
    'Final Fantasy XV': 'FFXV',
    'Final Fantasy Tactics': 'FFT',
    'Final Fantasy Tactics Advance': 'FFTA',
    'Vagrant Story': 'VagrS',
    'Final Fantasy Type-0': 'Type0',
    'Final Fantasy Crystal Chronicles': 'FFCC',
    'Final Fantasy Mystic Quest': 'FFMQ',
    'Final Fantasy Adventure': 'FFA',
    'The Final Fantasy Legend': 'FFL',
    'Final Fantasy Legend II': 'FFL2',
    'Final Fantasy Legend III': 'FFL3',
    'Final Fantasy: The 4 Heroes of Light': 'T4HoL',
    'Bravely Default': 'BravelyD',
    'Final Fantasy Dimensions': 'FFD',
    'Mobius Final Fantasy': 'Mobius',
    'Final Fantasy: The Spirits With': 'FFTSW',
}

optCodenames = {
    # These are "high risk" and likely to clash with the
    # intended codename when used as a categoric ancestor
    # but could be useful for another script!
    'Dissidia Final Fantasy (2008)': 'DFF2008',
    'Dissidia 012 Final Fantasy': 'D012',
    'Dissidia Final Fantasy NT': 'DFFNT',
    'Dissidia Final Fantasy Opera Omnia': 'DFFOO',
    'Theatrhythm Final Fantasy': 'TFF',
    'Pictlogica Final Fantasy': 'PFF',
    'Final Fantasy Airborne Brigade': 'FFAB',
    'Final Fantasy Artniks': 'Artniks',
    'Final Fantasy All the Bravest': 'FFATB',
    'Final Fantasy Record Keeper': 'FFRK',
    'Final Fantasy Explorers': 'FFE',
    'Final Fantasy World Wide Words': 'FFWWW',
    'Final Fantasy Brave Exvius': 'FFBE',
    'World of Final Fantasy': 'WoFF',
    'Chocobo Racing': 'ChocoR',
    'Chocobo no Fushigi na Dungeon': 'ChocoD',
    'Dice de Chocobo': 'DdC',
    'Chocobo Panic': 'ChocoP',
    'Final Fantasy: Unlimited': 'FFU',
    'Final Fantasy Trading Card Game': 'FFTCG'
}

YYYY = 2007
MM = 6
DD = 3

ancestorMemo = {}

def categoricAncestor(page, depth):
    # Returns the *categoric ancestor* of the page,
    # the highest-level category which has a sideicon related to it,
    # if it exists and is unique, and False otherwise.
    if page in ancestorMemo:
        return ancestorMemo[page]
    # print('\t' * depth + page.title())
    MAX_RECURSION_DEPTH = 20
    ancestors = set()
    for cat in textlib.getCategoryLinks(page.text):
        tit = cat.title()[9:]
        if tit in codenames:
            ancestors.add(cat)
            # sys.stdout.write('\t' * (depth + 1) + cat.title() + ' *\n')
            continue
        elif depth < MAX_RECURSION_DEPTH:
            thisAnc = categoricAncestor(cat, depth + 1)
            if thisAnc:
                ancestors.add(thisAnc)
    if len(ancestors) == 1:
        ancestorMemo[page] = list(ancestors)[0]
        return categoricAncestor(page, 0)
    ancestorMemo[page] = False
    return False

def startDate(page, year, month, day):
    stamp = page.getVersionHistory()[-1].timestamp
    if random.uniform(0, 1) < .01: # Random progress check!
        print(str(stamp))
    if stamp.year != year:
        return stamp.year > year
    if stamp.month != month:
        return stamp.month > month
    return stamp.day >= stamp.day

def printAncestorMemo():
    # for debugging
    return ancestorMemo

def primecheck(page, innerSideiconContent):
    cat = categoricAncestor(page, 0)
    if cat:
        tit = cat.title()[9:]
        if tit not in codenames:
            return
        codename = codenames[tit]
        # print('\t' + codename)
        # print('\t' + innerSideiconContent)
        if "|" + codename + "}}" in innerSideiconContent:
            return innerSideiconContent.replace("|" + codename + "}}", "|prime=" + codename + "}}")
        elif "|" + codename + "|" in innerSideiconContent:
            return innerSideiconContent.replace("|" + codename + "|", "|prime=" + codename + "|")
        else:
            print("Warning: " + codename + " not found in " + page.title() + "!")
    return innerSideiconContent
 
def sideicon(page):
    if "prime=" in page.text or not startDate(page, YYYY, MM, DD):
        return
    i = 0
    innerSideiconContent = '{{sideicon'
    while page.text.find('{{sideicon', i) != -1:
        i = page.text.find('{{sideicon', i)
        j = page.text.find('}}', i)
        innerSideiconContent = innerSideiconContent + '|' + page.text[i+11:j]
        page.text = page.text[:i] + page.text[j+2:]
    innerSideiconContent = innerSideiconContent + '}}'
    innerSideiconContent = primecheck(page, innerSideiconContent) 
    # print('\t' + innerSideiconContent)
    while page.text[:1] == '\n':
        page.text = page.text[1:]
    page.text = innerSideiconContent + '\n' + page.text
    page.save(u'Reformatting {{sideicon}} with categoric ancestors')

def main(*args):
    gen = pagegenerators.ReferringPageGenerator(pywikibot.Page(site, 'Template:Sideicon'), onlyTemplateInclusion=True)
    for page in gen:
        sideicon(page)

if __name__ == "__main__":
    main()
