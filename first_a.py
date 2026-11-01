import bisect
def search(it, key):
    node = it.root
    while True:
        it.reads += 1
        i = bisect.bisect_left(node.keys, key)
        if i < len(node.keys) and node.keys[i] == key:
            return True
        if node.leaf:
            return False
        node = node.children[i]