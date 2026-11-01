#Part D2: the # CASE ? labels
#n _delete and _fill, replace each # CASE ?
# ------------------------------------------------------------ delete
import bisect
def delete(self, key):
    self._delete(self.root, key)
    if not self.root.keys and not self.root.leaf:  # ROOT RULE: root empty after a merge,
        self.root = self.root.children[0]  # its only child becomes the root (height - 1)


def _delete(self, node, key):
    t = self.t
    self.reads += 1
    i = bisect.bisect_left(node.keys, key)
    found = i < len(node.keys) and node.keys[i] == key

    if node.leaf:  # CASE 1: key is in a leaf, just remove it
        if found:
            node.keys.pop(i)
            self.writes += 1
        return

    if found:  # key is in this internal node
        left, right = node.children[i], node.children[i + 1]

        if len(left.keys) >= t:  # CASE 2a: left child has >= t keys,
            pred = self._max_key(left)  # replace key by its predecessor
            node.keys[i] = pred  # and delete the predecessor from the left child
            self._delete(left, pred)

        elif len(right.keys) >= t:  # CASE 2b: right child has >= t keys,
            succ = self._min_key(right)  # replace key by its successor
            node.keys[i] = succ  # and delete the successor from the right child
            self._delete(right, succ)

        else:  # CASE 2c: both children have only t-1 keys,
            self._merge(node, i)  # merge left + key + right into one node
            self._delete(left, key)  # then delete the key from the merged node
        return

    # key is not in this node: descend into child i
    child = node.children[i]  # CASE 3 entry: check the child before entering it
    if len(child.keys) == t - 1:  # child is minimal, so give it an extra key first
        i = self._fill(node, i)  # (3a borrow or 3b merge, done in _fill)
    self._delete(node.children[i], key)


def _max_key(self, node):
    while not node.leaf:
        self.reads += 1
        node = node.children[-1]
    return node.keys[-1]


def _min_key(self, node):
    while not node.leaf:
        self.reads += 1
        node = node.children[0]
    return node.keys[0]

def _fill(self, node, i):

    t = self.t
    if i > 0 and len(node.children[i - 1].keys) >= t:
        child, sib = node.children[i], node.children[i - 1]
        child.keys.insert(0, node.keys[i - 1])
        node.keys[i - 1] = sib.keys.pop()
        if not sib.leaf:
            child.children.insert(0, sib.children.pop())
        self.writes += 3
        return i
    if i < len(node.children) - 1 and len(node.children[i + 1].keys) >= t:
        child, sib = node.children[i], node.children[i + 1]
        child.keys.append(node.keys[i])
        node.keys[i] = sib.keys.pop(0)
        if not sib.leaf:
            child.children.append(sib.children.pop(0))
        self.writes += 3
        return i
    if i < len(node.children) - 1:
        self._merge(node, i)
        return i
    self._merge(node, i - 1)
    return i - 1
def _merge(self, node, i):

    left, right = node.children[i], node.children[i + 1]
    left.keys.append(node.keys.pop(i))
    left.keys.extend(right.keys)
    left.children.extend(right.children)
    node.children.pop(i + 1)
    self.merges += 1
    self.writes += 2