# TODO: Make icons work

import urllib.request, json, databases.ffxiv_truncated #BEWARE
from update_module import publish
from databases.ffxiv import databases as xivdb
# Need PIP for urllib and json
xivdb = xivdb()

DEBUG = False
VERBOSE = False

def decode(url):
    req = urllib.request.Request(url, headers={"User-Agent": "JSON reader"})
    with urllib.request.urlopen(req) as data:
        return json.loads(data.read().decode())

def recover_ids(url, norepeat):
    if VERBOSE:
        print("\tRecovering IDs...")
    ids = []
    names = []
    for unit in decode(url):
        if not norepeat or not 'name' in unit or not unit['name'] in names:
            ids.append(unit['id'])
        elif norepeat and VERBOSE:
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
    elif VERBOSE:
        print("\t\tdon't know what to do with " + str(type(v)) + ":")
        print("\t\t\t" + str(v))
        return None
    else:
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

def parse_run(db, url, keys, norepeat):
    lua = "return {\n"
    db_count = 1
    ids = recover_ids(url, norepeat)
    print("\tDecoding data...")
    debug_halt_counter = 0
    index = ""
    subdivision = "1"

    for uid in ids:
        if DEBUG and debug_halt_counter > 10:
            break
        if uid % 100 == 0 and VERBOSE:
            print("\t\tCurrently running UID " + str(uid))

        v = decode(url + "/" + str(uid))
        if 'is_in_game' in v and v['is_in_game'] == 0:
            continue
        debug_halt_counter += 1
        
        index += "[\"" + v['name'] + "\"]="+str(uid)+",\n"
        lua += "[" + str(uid) + "]=" + read_table(v, keys) + ",\n"
 
        if len(lua) > 1500000:
            lua += "}"
            if VERBOSE:
                print("\t\tPublishing DB " + str(db_count))
            publish("Module:FFXIV Data/" + db + "/" + str(db_count), lua)
            db_count += 1
            subdivision += ", " + str(uid + 1)
            lua = "return {"

    lua += "}"
    publish("Module:FFXIV Data/" + db + "/" + str(db_count), lua)
    publish_index(db, db_count, subdivision, index)

def publish_index(db, db_count, subdivision, index):
    lua = "DB_COUNT = " + str(db_count) + "\n"
    lua += "data = {SUBDIVISION = {" + subdivision + "}}\n"
    lua += "for i=1,DB_COUNT do data[i] = mw.loadData(\"Module:FFXIV Data/" + db + "/\" .. i) end\n"
    lua += "data.index={" + index + "}\n"
    lua += "return data"
    publish("Module:FFXIV Data/" + db, lua)

def main(*args):
    for db in xivdb:
        if db != "instance" and DEBUG:
            continue
        if VERBOSE:
            print("Running parser on database " + db + ":")
        norepeat = False
        if 'norepeat' in xivdb[db] and xivdb[db]['norepeat']:
            norepeat = True
        parse_run(db, xivdb[db]['url'], xivdb[db]['keys'], norepeat)
        if VERBOSE:
            print("\tDone!")

if __name__ == "__main__":
    main()
