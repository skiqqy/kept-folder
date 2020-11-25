def append_log(path, key, val, misc=None):
    entry = key + "^" + val
    if misc != None:
        entry += "^" + misc
    entry += "\n"
    f = open(path, "a")
    f.write(entry)

def write_keyval(key, val, misc=None, path="disk/keys/log"):
    append_log(path, key, val, misc)

def search_log(path, key):
    f = open(path, "r")
    f = f.read().splitlines()
    for line in f:
        if line.split("^")[0] == key:
            return line
    return None

def search_key(key, path="disk/keys/log"):
    return search_log(path, key)

if __name__ == '__main__':
    write_keyval("key1", "val1", path="test/keys/log")
    write_keyval("key2", "val2", "misc", path="test/keys/log")
    print(search_log("test/keys/log", "key1"))
    print(search_log("test/keys/log", "key2"))
    print(search_log("test/keys/log", "key3"))
