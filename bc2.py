#Part C2: _split_child (inside class BTree)
import bisect
def _split_child(it, parent, i):
    t = it.t
    y = parent.children[i]
    z = BNode(y.leaf)
    median = y.keys[t - 1]
    z.keys = y.keys[t:]
    y.keys = y.keys[:t - 1]
    if not y.leaf:
        z.children = y.children[t:]
        y.children = y.children[:t]
    parent.keys.insert(i, median)
    parent.children.insert(i + 1, z)
    it.splits += 1
    it.writes += 3