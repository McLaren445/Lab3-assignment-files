import bisect
import time
import random
class BPlusNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.next = None
        self.records = []

class BPlusTree:
    def __init__(self, t=64):
        self.t = t
        self.root = BPlusNode(leaf=True)
        self.reads = 0
    def bulk_load(self, sorted_pairs, fill=1.0):
        max_keys = int((2 * self.t - 1) * fill)
        if max_keys < 2: max_keys = 2
        leaves = []
        for i in range(0, len(sorted_pairs), max_keys):
            leaf = BPlusNode(leaf=True)
            leaf.records = sorted_pairs[i:i + max_keys]
            leaf.keys = [pair[0] for pair in leaf.records]
            leaves.append(leaf)

        for i in range(len(leaves) - 1):
            leaves[i].next = leaves[i + 1]

        current_level = leaves
        while len(current_level) > 1:
            parents = []

            for i in range(0, len(current_level), self.t):
                parent = BPlusNode(leaf=False)
                children = current_level[i:i + self.t]
                parent.children = children

                parent.keys = [child.keys[0] for child in children[1:]]
                parents.append(parent)
            current_level = parents
        self.root = current_level[0]
    def search(self, key):
        self.reads = 0
        node = self.root
        while not node.leaf:
            self.reads += 1
            i = bisect.bisect_right(node.keys, key)
            node = node.children[i]
        self.reads += 1
        i = bisect.bisect_left(node.keys, key)
        if i < len(node.keys) and node.keys[i] == key:
            return node.records[i]
        return None
    def range(self, lo, hi):
        self.reads = 0
        node = self.root
        while not node.leaf:
            self.reads += 1
            i = bisect.bisect_right(node.keys, lo)
            node = node.children[i]
        results = []
        while node:
            self.reads += 1
            for k, rec in node.records:
                if k > hi:
                    return results
                if k >= lo:
                    results.append((k, rec))
            node = node.next
        return results