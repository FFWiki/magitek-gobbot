import pywikibot

def clean(lua):
    while ",," in lua:
        lua = lua.replace(",,",",")
    return lua.replace("{,","{")

def publish(module, lua):
    site = pywikibot.Site()
    page = pywikibot.Page(site, module)
    page.text = clean(lua)
    print(page.text)
    page.save(u"Updating module")
