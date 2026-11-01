#Part B2: range (inside class BTree)
import bisect
def range(it, lo, hi):
    out = []
    def go(node):
        it.reads += 1
        i = bisect.bisect_left(node.keys, lo)
        n = len(node.keys)
        while i < n:
            if not node.leaf:
                go(node.children[i])
            k = node.keys[i]
            if k > hi:
                return
            out.append(k)
            i += 1
        if not node.leaf:
            go(node.children[n])
    go(it.root)
    return out