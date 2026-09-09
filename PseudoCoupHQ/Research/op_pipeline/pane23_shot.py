#!/usr/bin/env python3
"""pane23_shot.py -- TEST RIG ONLY.  Not part of the dashboard.

Photographs the views of panes 2 and 3 through pane23_shot.html, in
headless Chrome, against the real artifacts served with byte ranges.

    /tmp/reconnect_venv/bin/python3 pane23_shot.py <out-dir>
"""

import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(HERE)
PORT = 8973
CHROME = "/usr/bin/google-chrome"

SHOTS = [
    ("selector_full_population.png", "?pane=units", "pane 1's selector "
     "with the signature menu filled over the whole population"),
    ("selector_language_cpp.png", "?pane=units&lang=cpp&sigpick=1",
     "the selector narrowed to one language and one type signature"),
    ("opcode_index_ret.png", "?pane=opcodes&opcode=ret",
     "the arch opcode index on the opcode that is in the most units"),
    ("opcode_index_movss.png", "?pane=opcodes&opcode=movss",
     "the arch opcode index on a narrower opcode"),
    ("glyph_selector.png", "?pane=units&labels=glyph",
     "the selector with every operator label replaced by a glyph"),
    ("glyph_opcode_index.png", "?pane=opcodes&opcode=ret&labels=glyph",
     "the arch opcode index with every operator label replaced by a glyph"),
    ("seeded_sample.png", "?pane=units#seed=20260903",
     "the seeded sampler: the seed in the address selected this unit"),
]


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    srv = subprocess.Popen(
        [sys.executable, os.path.join(HERE, "dashboard_test_server.py"),
         RESEARCH, str(PORT)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    srv.stdout.readline()
    time.sleep(0.6)
    try:
        for name, query, what in SHOTS:
            url = ("http://127.0.0.1:%d/op_pipeline/pane23_shot.html%s"
                   % (PORT, query))
            profile = tempfile.mkdtemp(prefix="pane23_shot_")
            path = os.path.join(out, name)
            subprocess.run(
                [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                 "--user-data-dir=" + profile,
                 "--window-size=1600,1400",
                 "--virtual-time-budget=300000",
                 "--screenshot=" + path, url],
                capture_output=True, text=True, timeout=600)
            shutil.rmtree(profile, ignore_errors=True)
            size = os.path.getsize(path) if os.path.exists(path) else 0
            print("%-32s %9d bytes  %s" % (name, size, what))
    finally:
        srv.send_signal(signal.SIGTERM)
        srv.wait(timeout=10)
    return 0


if __name__ == "__main__":
    sys.exit(main())
