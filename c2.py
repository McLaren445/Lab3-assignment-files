#Part C3: insert and _insert_nonfull (inside class BTree)
import bisect
def search_quiet(it, key):
    node = it.root
    while True:
        i = bisect.bisect_left(node.keys, key)
        if i < len(node.keys) and node.keys[i] == key:
            return True
        if node.leaf:
            return False
        node = node.children[i]
def insert(it, key):
    if it.search_quiet(key):
        return
    root = it.root
    if len(root.keys) == 2 * it.t - 1:
        new_root = BNode(False)
        new_root.children.append(root)
        it.root = new_root
        it._split_child(new_root, 0)
        root = new_root
    it._insert_nonfull(root, key)
def _insert_nonfull(it, node, key):
    t = it.t
    while True:
        i = bisect.bisect_left(node.keys, key)
        if node.leaf:
            node.keys.insert(i, key)
            it.writes += 1
            return
        if len(node.children[i].keys) == 2 * t - 1:
            it._split_child(node, i)
            if key > node.keys[i]:
                i += 1
        node = node.children[i]