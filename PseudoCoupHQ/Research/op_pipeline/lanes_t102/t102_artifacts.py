#!/usr/bin/env python3
"""t102 bank -- artifact existence/size/mtime/git-log check, run inside Airlock.
Reads a manifest of (task, node, path) triples and reports, per path:
  exists, size, mtime, and git log --follow -1 (committed / not).
Paths outside any mount are reported as OUT_OF_SANDBOX (checked by the
coordinator on the host separately -- Airlock's own repo is not mounted
into any instance, by the sandbox's own security design).
"""
import json
import os
import subprocess
import sys

HQ = "PseudoCoupHQ"
GRAPHS = "PseudoCoupGraphs"

def git_log_follow(repo, relpath):
    try:
        out = subprocess.run(
            ["git", "-C", repo, "log", "--follow", "-1", "--format=%H %cI %s", "--", relpath],
            capture_output=True, text=True, timeout=20,
        )
        line = out.stdout.strip()
        return line if line else "NOT_COMMITTED (no git log entry)"
    except Exception as e:
        return "GIT_ERROR: %r" % e

def check_one(task, node, path, note=""):
    row = {"task": task, "node": node, "path": path, "note": note}
    if path.startswith(HQ):
        repo = HQ
        rel = os.path.relpath(path, HQ)
    elif path.startswith(GRAPHS):
        repo = GRAPHS
        rel = os.path.relpath(path, GRAPHS)
    else:
        row["exists_in_instance"] = "OUT_OF_SANDBOX"
        row["git"] = "OUT_OF_SANDBOX -- not mounted; coordinator checks on host"
        return row
    exists = os.path.exists(path)
    row["exists_in_instance"] = exists
    if exists:
        st = os.stat(path)
        if os.path.isdir(path):
            row["size"] = "DIR (%d entries)" % len(os.listdir(path))
        else:
            row["size"] = st.st_size
        row["mtime"] = __import__("datetime").datetime.utcfromtimestamp(st.st_mtime).isoformat() + "Z"
        row["git"] = git_log_follow(repo, rel)
    else:
        row["size"] = None
        row["mtime"] = None
        row["git"] = git_log_follow(repo, rel)
    return row

def main():
    manifest = json.load(open(sys.argv[1]))
    results = []
    for entry in manifest:
        results.append(check_one(entry["task"], entry["node"], entry["path"], entry.get("note", "")))
    out = {"results": results}
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    # print a compact table too
    for r in results:
        print("%-6s %-70s exists=%-6s size=%-12s git=%s" % (
            r["task"], r["path"], r["exists_in_instance"], r.get("size"), r["git"][:90]))

if __name__ == "__main__":
    main()
