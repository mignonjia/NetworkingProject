import hashlib
f = "database.txt"
def filehash(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        content = f.read(4096)
        h.update(content)
    print(h.hexdigest())
    return h.hexdigest()

if __name__ == '__main__':
    filehash(f)