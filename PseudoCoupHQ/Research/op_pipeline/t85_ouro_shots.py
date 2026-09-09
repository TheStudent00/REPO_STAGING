#!/usr/bin/env python3
"""t85_ouro_shots.py -- drive the REAL Ourobrowser over the dashboard and
photograph it.  TASK 85.

This is the ONE thing in task 85 that is not an Airlock lane: the browser
IS the viewer of the deliverable, so looking at the deliverable happens
on the host.  It computes nothing the page does not compute for itself.

It imports `Ourobrowser/browser_engine.py` and does not
edit it: the engine belongs to the owner and that work is paused.

usage:
    cd Ourobrowser && \
    LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1 \
    python3 <this file>
"""

import os
import resource
import sys

OURO = os.path.expanduser("Ourobrowser")
PAGE = os.path.expanduser(
    "PseudoCoupHQ/Research/op_pipeline/dashboard_ouro.html")
SHOTS = os.path.expanduser(
    "PseudoCoupHQ/DevComms/screens/log_191")

sys.path.insert(0, OURO)

from PyQt6.QtCore import QTimer, QUrl                       # noqa: E402
from PyQt6.QtWidgets import QApplication                    # noqa: E402
from PyQt6.QtWebEngineCore import QWebEngineUrlScheme       # noqa: E402

import browser_engine                                       # noqa: E402


def click(expression):
    """press the element whose click wire form is `expression`.

    The wire form is the ATTRIBUTE `data-python-onclick`, which is what
    the engine rewrites `onclick="python:…"` into (log_184 §2.4).

    The first cut of this function built a CSS attribute selector by
    string substitution, and every moment expression carries apostrophes
    (`ouro_moment('20')`), which closed the JavaScript string literal
    around the selector.  Every tab click worked and every MOMENT click
    silently returned nothing.  Found by running it: three consecutive
    screenshots came back byte-identical.  The fix walks the attribute
    values and compares, so no expression is ever spliced into a
    selector.  This is the rig's defect, not the page's.
    """
    return ('(function(){'
            'var all=document.querySelectorAll("[data-python-onclick]");'
            'for(var i=0;i<all.length;i++){'
            'if(all[i].getAttribute("data-python-onclick")==="%s")'
            '{all[i].click();return "clicked";}}'
            'return "MISSING";})()' % expression)


def selected_moment():
    """what the page itself says the selected moment is -- read back off
    the rendered chronology, so a click is verified, not assumed."""
    return ('(function(){var e=document.querySelector(".momentnow");'
            'return e?e.textContent:"NO CHRONOLOGY ON THE PAGE";})()')


#: what to do, in order.  Each step is (name, javascript-or-None).
#: A step with a name and no javascript is a photograph.
STEPS = [
    ("shot", "tab5_stats_now"),
    ("click", click("ouro_pane(2)")),
    ("shot", "tab2_selector_now"),
    ("click", click("ouro_pane(4)")),
    ("shot", "tab4_coverage_now"),
    # ONE moment, chosen once, applied to the page: a commit before any
    # artifact was tracked.
    ("click", click("ouro_moment('20')")),
    ("read", selected_moment()),
    ("shot", "tab4_coverage_at_2026_08_25_refused"),
    ("click", click("ouro_pane(1)")),
    ("shot", "tab1_unitviewer_at_2026_08_25_refused"),
    ("click", click("ouro_pane(5)")),
    ("shot", "tab5_stats_at_2026_08_25_refused"),
    # a moment where the corpus IS tracked: the same tabs fill in.
    ("click", click("ouro_moment('35')")),
    ("read", selected_moment()),
    ("shot", "tab5_stats_at_round12"),
    ("click", click("ouro_pane(1)")),
    ("shot", "tab1_unitviewer_at_round12"),
    ("click", click("ouro_pane(3)")),
    ("shot", "tab3_opcode_at_round12"),
    ("click", click("ouro_pane(4)")),
    ("shot", "tab4_coverage_at_round12_refused"),
    # the last banked round, where the coverage pane fills in too.
    ("click", click("ouro_moment('38')")),
    ("read", selected_moment()),
    ("shot", "tab4_coverage_at_round14"),
    ("click", click("ouro_pane(2)")),
    ("shot", "tab2_selector_at_round14"),
    ("click", click("ouro_moment('now')")),
    ("read", selected_moment()),
    ("shot", "tab2_selector_back_at_now"),
]


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def run():
    scheme = QWebEngineUrlScheme(b"ourobrowser")
    scheme.setSyntax(QWebEngineUrlScheme.Syntax.HostAndPort)
    scheme.setFlags(QWebEngineUrlScheme.Flag.SecureScheme
                    | QWebEngineUrlScheme.Flag.LocalScheme
                    | QWebEngineUrlScheme.Flag.LocalAccessAllowed)
    QWebEngineUrlScheme.registerScheme(scheme)

    os.makedirs(SHOTS, exist_ok=True)
    app = QApplication(sys.argv[:1])
    window = browser_engine.OurobrowserWindow(start_page="/" + PAGE)
    window.resize(1400, 1000)
    window.show()

    state = {"at": 0}

    def advance():
        if state["at"] >= len(STEPS):
            print("[rig] peak resident size of the python side: %.1f MB"
                  % peak_mb())
            QTimer.singleShot(200, app.quit)
            return
        kind, payload = STEPS[state["at"]]
        state["at"] += 1
        if kind == "shot":
            path = os.path.join(SHOTS, payload + ".png")
            image = window.browser.grab()
            saved = image.save(path)
            print("[rig] shot %s -> %s (%dx%d, saved=%s, %d bytes)"
                  % (payload, path, image.width(), image.height(), saved,
                     os.path.getsize(path) if os.path.exists(path) else 0))
            QTimer.singleShot(400, advance)
        else:
            def answered(value, kind=kind):
                print("[rig] %s -> %s" % (kind, value))
                QTimer.singleShot(1500 if kind == "click" else 200, advance)
            window.browser.page().runJavaScript(payload, answered)

    def loaded(ok):
        print("[rig] loadFinished ok=%s" % ok)
        QTimer.singleShot(1500, advance)

    window.browser.loadFinished.connect(loaded)
    window.browser.setUrl(QUrl("ourobrowser://local//" + PAGE))
    app.exec()


if __name__ == "__main__":
    run()
