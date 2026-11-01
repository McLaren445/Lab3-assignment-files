#Part E2: running the benchmark (separate file benchmark.py)
import bisect, random, time
from lab3b import BTree
from rbtree import RBTree
N, PROBES = 100_000, 5_000
class SortedList:
    def __init__(self):
        self.a = []
    def insert(self, k):
        bisect.insort(self.a, k)
    def search(self, k):
        i = bisect.bisect_left(self.a, k)
        return i < len(self.a) and self.a[i] == k
rng = random.Random(2026)
keys = rng.sample(range(10 * N), N)
probe = [rng.choice(keys) for _ in range(PROBES)]

for t in (2, 4, 16, 64, 256):
    print(f"B-tree t={t}", run(lambda t=t: BTree(t), keys, probe))
print("Red-Black", run(RBTree, keys, probe))
print("Sorted list", run(SortedList, keys, probe))