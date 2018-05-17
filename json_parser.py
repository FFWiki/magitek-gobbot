# TODO: Make icons work

import urllib.request, json, databases 
xivdb = databases.databases()
DEBUG = False

def decode(url):
    with urllib.request.urlopen(url) as data:
        return json.loads(data.read().decode())

def recover_ids(url, norepeat):
    print("\tRecovering IDs...")
    ids = []
    names = []
    for unit in decode(url):
        if not norepeat or not 'name' in unit or not unit['name'] in names:
            ids.append(unit['id'])
        elif norepeat:
            print("\t\tTEST MESSAGE: Norepeating " + unit['name'])
    return ids

def clean(s):
    return s.replace("[","").replace("]","")

def tostr(v, keys):
    if isinstance(v, bool):
        return (v and 1) or None
    elif isinstance(v, int) or isinstance(v, float):
        if v == 0:
            return None
        return str(v)
    elif isinstance(v, dict):
        return read_table(v, keys)
    elif isinstance(v, list):
        return read_array(v, keys)
    elif isinstance(v, str):
        return "[[" + clean(v) + "]]"
    elif v is None or v == []:
        return None
    else:
        print("\t\tdon't know what to do with " + str(type(v)) + ":")
        print("\t\t\t" + str(v))
        return None

def read_array(v, keys):
    lua = "{"
    for entry in v:
        lua += read_table(entry, keys) + ","
    lua += "},"
    return lua

def read_table(v, keys):
    lua = "{"
    for k in keys:
        if k in v:
            s = tostr(v[k], keys[k])
            if s is not None:
                lua += k + "=" + s + ","
    lua += "}"
    return lua

def parse_run(url, keys, norepeat):
    lua = "return {data={"
    index = ""
    ids = recover_ids(url, norepeat)
    print("\tDecoding data...")
    debug_halt_counter = 0
    for uid in ids:
        if DEBUG and debug_halt_counter > 10:
            break
        if uid % 100 == 0:
            print("\t\tCurrently running UID " + str(uid))
        uid = str(uid)

        v = decode(url + "/" + uid)
        if 'is_in_game' in v and v['is_in_game'] == 0:
            continue
        debug_halt_counter += 1
        
        index += "[\"" + v['name'] + "\"]="+uid+","
        lua += "[" + uid + "]=" + read_table(v, keys) + ","
    lua += "},index={" + index + "}}"
    return lua

def clean_lua(lua):
    return lua.replace(",,",",").replace("{,","{")

for db in xivdb:
    if db != "instance":
        continue
    print("Running parser on database " + db + ":")
    norepeat = False
    if 'norepeat' in xivdb[db] and xivdb[db]['norepeat']:
        norepeat = True
    s = parse_run(xivdb[db]['url'], xivdb[db]['keys'], norepeat)
    s = clean_lua(s)
    if len(s) > 2097150:
        print('\tPossibility of MediaWiki file overflow error.')
    print("\tPrinting to file...")
    with open('lua/' + db + '.lua', 'w') as f:
        f.write(s)
    print("\tDone!")
