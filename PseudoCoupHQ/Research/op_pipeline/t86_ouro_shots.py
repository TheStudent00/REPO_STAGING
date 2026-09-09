#!/usr/bin/env python3
"""t86_ouro_shots.py -- drive the REAL Ourobrowser over the dashboard and
photograph it.  TASK 86.

This is the ONE thing in task 86 that is not an Airlock lane: the browser
IS the viewer of the deliverable, so looking at the deliverable happens
on the host.  It computes nothing the page does not compute for itself.

It imports `Ourobrowser/browser_engine.py` and does not
edit it: the engine belongs to the owner and that work is paused.

THE MOMENT KEYS BELOW ARE COMMIT IDENTITIES, not positions.  Task 85's
rig clicked `ouro_moment('20')` -- an index into a curated list of 39
steps.  A moment is now a commit, so the key IS the commit, which also
means these clicks keep working while the repository's own daemon adds
commits underneath the page.  Every sha here was read off
`t86_all_panes.json`, the full pass's own product.

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
    "PseudoCoupHQ/DevComms/screens/log_192")

sys.path.insert(0, OURO)

from PyQt6.QtCore import QTimer, QUrl                       # noqa: E402
from PyQt6.QtWidgets import QApplication                    # noqa: E402
from PyQt6.QtWebEngineCore import QWebEngineUrlScheme       # noqa: E402

import browser_engine                                       # noqa: E402


def click(expression):
    """press the element whose click wire form is `expression`.

    The wire form is the ATTRIBUTE `data-python-onclick`, which is what
    the engine rewrites `onclick="python:…"` into (log_184 §2.4).  The
    attribute values are walked and compared rather than spliced into a
    CSS selector, because every moment expression carries apostrophes --
    task 85's rig defect, kept fixed here.
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


def window_line():
    """the commit row's own ceiling line, read back off the page, so a
    day click is verified to have MOVED THE WINDOW."""
    return ('(function(){var all=document.querySelectorAll(".scalename");'
            'return all.length>1?all[1].textContent:"NO COMMIT ROW";})()')


#: three commits, and one day.  The commits were read off
#: `t86_all_panes.json`: one before any artifact was tracked, one where
#: the corpus is tracked but the compiler graph is not, and one where
#: every pane fills in.
EARLY = "4f175cbc00be"     # 2026-08-19 09:05, nothing tracked yet
MIDDLE = "4457428eef88"    # 2026-09-03 03:18, corpus tracked, graph not
MIDDLE_DAY = "2026-09-03"
LATE = "b9ca4ac54351"      # 2026-09-04 14:45, every pane fills in
LATE_DAY = "2026-09-04"
DAY = "2026-08-19"

STEPS = [
    ("shot", "tab5_stats_now"),
    ("click", click("ouro_pane(2)")),
    ("shot", "tab2_selector_now"),
    ("click", click("ouro_pane(1)")),
    ("shot", "tab1_unitviewer_now"),
    # THE DAY ROW MOVES THE WINDOW AND SELECTS NOTHING.  The moment
    # read back after this click must still be `now`.
    ("click", click("ouro_window('%s')" % DAY)),
    ("read", selected_moment()),
    ("read", window_line()),
    ("shot", "day_click_moves_the_window_selects_nothing"),
    # ONE moment change, and more than one pane is different: tabs 1 and
    # 5 both change against their `now` photographs above.
    ("click", click("ouro_moment('%s')" % EARLY)),
    ("read", selected_moment()),
    ("shot", "tab1_unitviewer_at_2026_08_19_refused"),
    ("click", click("ouro_pane(5)")),
    ("shot", "tab5_stats_at_2026_08_19_refused"),
    ("click", click("ouro_pane(4)")),
    ("shot", "tab4_coverage_at_2026_08_19_refused"),
    # a commit where the corpus IS tracked and the compiler graph is
    # not.  It is 750 commits away, so it is not in the drawn window:
    # the DAY row is how the window gets there.  Found by running --
    # the first pass of this rig clicked the commit straight and the
    # engine answered MISSING, because a tick that is not drawn cannot
    # be pressed.  That is the stated ceiling working, not a fault.
    ("click", click("ouro_window('%s')" % MIDDLE_DAY)),
    ("read", window_line()),
    # 2026-09-03 carries 521 commits, so its first windowful does not
    # reach 03:18 either: one shift of the window does.  This is the
    # second thing the run found -- a day is not one windowful, and the
    # two shift controls are what make every commit reachable.
    ("click", click("ouro_window('later')")),
    ("read", window_line()),
    ("click", click("ouro_moment('%s')" % MIDDLE)),
    ("read", selected_moment()),
    ("shot", "tab4_coverage_at_2026_09_03_0318_refused"),
    ("click", click("ouro_pane(1)")),
    ("shot", "tab1_unitviewer_at_2026_09_03_0318"),
    ("click", click("ouro_pane(5)")),
    ("shot", "tab5_stats_at_2026_09_03_0318"),
    # a commit where every pane fills in -- again by way of its day,
    # because it is another 440 commits on
    ("click", click("ouro_window('%s')" % LATE_DAY)),
    ("read", window_line()),
    ("click", click("ouro_moment('%s')" % LATE)),
    ("read", selected_moment()),
    ("shot", "tab5_stats_at_2026_09_04_1445"),
    ("click", click("ouro_pane(4)")),
    ("shot", "tab4_coverage_at_2026_09_04_1445"),
    ("click", click("ouro_pane(3)")),
    ("shot", "tab3_opcode_at_2026_09_04_1445"),
    ("click", click("ouro_moment('now')")),
    ("read", selected_moment()),
    ("shot", "tab3_opcode_back_at_now"),
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
                QTimer.singleShot(2500 if kind == "click" else 200, advance)
            window.browser.page().runJavaScript(payload, answered)

    def loaded(ok):
        print("[rig] loadFinished ok=%s" % ok)
        QTimer.singleShot(2000, advance)

    window.browser.loadFinished.connect(loaded)
    window.browser.setUrl(QUrl("ourobrowser://local//" + PAGE))
    app.exec()


if __name__ == "__main__":
    run()
