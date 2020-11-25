def append_log(path, key, val, misc=None):
    entry = key + ":" + val
    if misc != None:
        entry += ":" + misc
    entry += "\n"
    f = open(path, "a")
    f.write(entry)

def write_keyval(key, val, misc=None, path="disk/keys/log"):
    append_log(path, key, val, misc)

if __name__ == '__main__':
    write_keyval("key1", "val1", path="test/keys/log")
    write_keyval("key2", "val2", "misc", path="test/keys/log")
