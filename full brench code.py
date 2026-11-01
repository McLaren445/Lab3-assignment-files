import bisect
import random
import time
import matplotlib.pyplot as plt
from lab3b import BTree
from rbtree import RBTree   

N = 100_000
PROBES = 5_000
# sorted list of E1, E2, E3
class SortedList:
    def __init__(self):
        self.a = []

    def insert(self, k):
        bisect.insort(self.a, k)
    def search(self, k):
        i = bisect.bisect_left(self.a, k)
        return i < len(self.a) and self.a[i] == k
def run(make, keys, probe):
    t = make()
    start = time.perf_counter()
    for k in keys:
        t.insert(k)
    build_s = time.perf_counter() - start
    if hasattr(t, "reads"):
        t.reads = 0                                   
    start = time.perf_counter()
    for k in probe:
        t.search(k)
    search_us = (time.perf_counter() - start) / len(probe) * 1e6
    reads_per_search = t.reads / len(probe) if hasattr(t, "reads") else None
    height = t.height() if hasattr(t, "height") else None
    return build_s, search_us, reads_per_search, height

rng = random.Random(2026)
keys = rng.sample(range(10 * N), N)
probe = [rng.choice(keys) for _ in range(PROBES)]

ts = [2, 4, 16, 64, 256]

res = [run(lambda t=t: BTree(t), keys, probe) for t in ts]
rb = run(RBTree, keys, probe)
sl = run(SortedList, keys, probe)
rb_height = rb[3]

print(f"{'Structure':22}{'Build s':>10}{'Search us':>11}{'Reads':>8}{'Height':>8}")
for t, r in zip(ts, res):
    print(f"{'B-tree t = ' + str(t):22}{r[0]:10.3f}{r[1]:11.2f}{r[2]:8.2f}{r[3]:8d}")
print(f"{'Red-Black':22}{rb[0]:10.3f}{rb[1]:11.2f}{'n/a':>8}{rb[3]:8d}")
print(f"{'Sorted list + bisect':22}{sl[0]:10.3f}{sl[1]:11.2f}{'n/a':>8}{'n/a':>8}")

plt.figure()
plt.plot(ts, [r[3] for r in res], "o-", label="B-tree height")
plt.axhline(rb_height, color="red", linestyle="--", label="Red-Black height")
plt.xscale("log", base=2)
plt.xlabel("minimum degree t")
plt.ylabel("height")
plt.title("Height against t (n = 100,000)")
plt.legend()
plt.savefig("plot_height.png", dpi=150)

fig, ax1 = plt.subplots()
ax1.plot(ts, [r[2] for r in res], "o-", color="blue")
ax1.set_xscale("log", base=2)
ax1.set_xlabel("minimum degree t")
ax1.set_ylabel("average page reads", color="blue")

ax2 = ax1.twinx()
ax2.plot(ts, [r[1] for r in res], "s--", color="orange")
ax2.set_ylabel("microseconds per search", color="orange")
plt.title("Page reads and time per search against t")
fig.tight_layout()
plt.savefig("plot_reads_time.png", dpi=150)
print("Saved plot_height.png and plot_reads_time.png")