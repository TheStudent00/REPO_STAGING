#!/usr/bin/env python3
"""pane23_clickthrough.py -- TEST RIG ONLY.  Not part of the dashboard.

Runs pane23_clickthrough.html in headless Chrome against the real
artifacts and prints the transcript the page logs.  Two runs by default:

  1. ?labels=glyph -- THE SPELLING-BAN TEST.  Every operator label is
     replaced by a glyph and every pane, every selector menu entry and
     every arch opcode entry is clicked.  Nothing but a display label
     reads the token, so nothing may break.
  2. the same page with a seed in the address, twice, to show that a
     reload with the same seed selects the same unit.

The folder dialog of the File System Access API belongs to the operating
system and cannot be clicked by any automation here (log_176 section
4.3), so the page is driven through dashboard_test_shim.js over the
byte-range server, with dashboard_join.js, dashboard_loader.js and
dashboard_pane23.js used UNCHANGED.

    /tmp/reconnect_venv/bin/python3 pane23_clickthrough.py [seed]
"""

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(HERE)
PORT = 8971
CHROME = "/usr/bin/google-chrome"


def start_server():
    proc = subprocess.Popen(
        [sys.executable, os.path.join(HERE, "dashboard_test_server.py"),
         RESEARCH, str(PORT)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    line = proc.stdout.readline()
    sys.stdout.write("    " + line)
    return proc


def run(url, budget_ms):
    profile = tempfile.mkdtemp(prefix="pane23_chrome_")
    try:
        proc = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--user-data-dir=" + profile,
             "--virtual-time-budget=%d" % budget_ms,
             "--enable-logging=stderr", "--v=0", "--dump-dom", url],
            capture_output=True, text=True, timeout=budget_ms / 1000 + 240)
        return proc.stderr
    finally:
        shutil.rmtree(profile, ignore_errors=True)


# Chrome's stderr wraps a console line as: ... "MESSAGE", source: URL (N)
# The message itself contains double quotes (it carries json), so the
# match runs to the ", source:" tail rather than to the next quote.
LINE = re.compile(r'"(\[(?:walk|pane23|dashboard)\].*?)", source: ')


def transcript(stderr):
    out = []
    for m in LINE.finditer(stderr):
        out.append(m.group(1))
    return out


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20260903
    base = ("http://127.0.0.1:%d/op_pipeline/pane23_clickthrough.html"
            % PORT)
    srv = start_server()
    time.sleep(0.6)
    try:
        print("")
        print("=" * 72)
        print("RUN 1 -- the spelling-ban click-through, every label a glyph")
        print("=" * 72)
        err = run(base + "?labels=glyph", 900000)
        lines = transcript(err)
        for line in lines:
            print(line)
        report = None
        for line in lines:
            if line.startswith("[walk] DONE "):
                report = json.loads(line[len("[walk] DONE "):])

        print("")
        print("=" * 72)
        print("RUN 2 -- the seeded sampler: the SAME address loaded twice")
        print("         seed=%d, carried in the address hash" % seed)
        print("=" * 72)
        url2 = ("http://127.0.0.1:%d/op_pipeline/pane23_shot.html"
                "?pane=units&labels=glyph#seed=%d" % (PORT, seed))
        errs = []
        for i in (1, 2):
            e = run(url2, 300000)
            picks = [x for x in transcript(e) if "[pane23] seed" in x]
            for p in picks:
                print("load %d: %s" % (i, p))
            errs.append(picks)
        same = errs[0] == errs[1] and errs[0]
        print("")
        print("RELOAD DETERMINISM: %s"
              % ("SAME unit on both loads" if same
                 else "DIFFERENT -- the sampler is not reproducible"))

        print("")
        print("=" * 72)
        print("SUMMARY")
        print("=" * 72)
        if report:
            print(json.dumps(report, indent=1, sort_keys=True))
            return 0 if report.get("errors") == 0 and same else 1
        print("no [walk] DONE line was printed")
        return 1
    finally:
        srv.send_signal(signal.SIGTERM)
        srv.wait(timeout=10)


if __name__ == "__main__":
    sys.exit(main())
