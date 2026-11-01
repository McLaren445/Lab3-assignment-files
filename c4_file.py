#Part E1: run function for the benchmark
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