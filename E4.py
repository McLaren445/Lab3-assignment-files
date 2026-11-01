#Part E3: the two plots (add at the end of benchmark.py)
import matplotlib.pyplot as plt

ts = [2, 4, 16, 64, 256]
res = [run(lambda t=t: BTree(t), keys, probe) for t in ts]
rb_height = run(RBTree, keys, probe)[3]

plt.figure()
plt.plot(ts, [r[3] for r in res], "o-", label="B-tree height")
plt.axhline(rb_height, color="red", linestyle="--", label="Red-Black height")
plt.xscale("log", base=2)
plt.xlabel("minimum degree t")
plt.ylabel("height")
plt.legend()
plt.savefig("plot_height.png")

fig, ax1 = plt.subplots()
ax1.plot(ts, [r[2] for r in res], "o-", color="blue")
ax1.set_xscale("log", base=2)
ax1.set_xlabel("minimum degree t")
ax1.set_ylabel("average page reads", color="blue")
ax2 = ax1.twinx()
ax2.plot(ts, [r[1] for r in res], "s--", color="orange")
ax2.set_ylabel("microseconds per search", color="orange")
plt.savefig("plot_reads_time.png")