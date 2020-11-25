def append_log(path, key, val, misc=None):
    entry = key + "^" + val
    if misc != None:
        entry += "^" + misc
    entry += "\n"
    f = open(path, "a")
    f.write(entry)

def write_keyval(key, val, misc=None, path="disk/log/keys"):
    append_log(path, key, val, misc)

def search_log(path, key):
    f = open(path, "r")
    f = f.read().splitlines()
    for line in f:
        if line.split("^")[0] == key:
            return line
    return None

def search_key(key, path="disk/log/keys"):
    return search_log(path, key)

if __name__ == '__main__':
    write_keyval("key1", "val1", path="test/log/keys")
    write_keyval("key2", "val2", "misc", path="test/log/keys")
    print(search_log("test/log/keys", "key1"))
    print(search_log("test/log/keys", "key2"))
    print(search_log("test/log/keys", "key3"))
