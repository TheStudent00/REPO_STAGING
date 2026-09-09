#!/usr/bin/env python3
"""t93_ouro_shots.py -- drive the REAL Ourobrowser over the dashboard and
photograph PANE 4, THE DRAWING.  TASK 93.

This is the ONE thing in task 93 that is not an Airlock lane: the browser
IS the viewer of the deliverable, so looking at the deliverable happens on
the host.  It computes nothing the page does not compute for itself.

It imports `~/Programming/Ourobrowser/browser_engine.py` and does not edit
it: the engine belongs to the owner and that work is paused.

WHAT IT PHOTOGRAPHS, and why each shot exists
---------------------------------------------
  * pane 4 at the present moment, for GO -- the three figures over the go
    compiler: structure, dynamic, direction;
  * one go file held, so figure 1 draws that file's own connections
    alone and figure 2 marks it;
  * one probe's own walk, and one operator traced variant's own
    transitions;
  * pane 4 for C AND CPP (clang) -- a second compiler, a much larger
    tree, at the same moment;
  * pane 4 for RUST -- a compiler with a graph and NO probe traces, so
    figures 2 and 3 draw their refusal by name;
  * pane 4 at a SECOND MOMENT, an earlier commit, so the chronology is
    shown applying to the drawing.

THE MOMENT KEYS ARE COMMIT IDENTITIES, not positions (task 86's rule):
the key IS the commit, so these clicks keep working while the repository's
own daemon adds commits underneath the page.

usage:
    cd ~/Programming/Ourobrowser && \
    LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1 \
    python3 ~/Programming/PseudoCoupHQ/Research/op_pipeline/t93_ouro_shots.py \
        [<commit identity of the earlier moment>]
"""

import os
import resource
import subprocess
import sys

OURO = os.path.expanduser("~/Programming/Ourobrowser")
PAGE = os.path.expanduser(
    "~/Programming/PseudoCoupHQ/Research/op_pipeline/dashboard_ouro.html")
SHOTS = os.path.expanduser(
    "~/Programming/PseudoCoupHQ/DevComms/screens/log_198")

sys.path.insert(0, OURO)

from PyQt6.QtCore import QTimer, QUrl                       # noqa: E402
from PyQt6.QtWidgets import QApplication                    # noqa: E402

import browser_engine                                       # noqa: E402


def click(expression):
    """press the element whose click wire form is `expression`.

    The wire form is the ATTRIBUTE `data-python-onclick`, which is what
    the engine rewrites `onclick="python:…"` into.  The attribute values
    are walked and compared rather than spliced into a CSS selector,
    because every one of these expressions carries apostrophes.

    A MouseEvent is DISPATCHED rather than `.click()` called: `click()`
    is a method of HTMLElement and an SVG element does not have it
    (measured -- "TypeError: all[i].click is not a function" on the
    first pass of this rig, on the file boxes of figure 1).  A person
    pressing the box works either way, because the engine's own listener
    is delegated from `document` and a real press bubbles; only a
    synthetic press had to be spelt this way.
    """
    return ('(function(){'
            'var all=document.querySelectorAll("[data-python-onclick]");'
            'for(var i=0;i<all.length;i++){'
            'if(all[i].getAttribute("data-python-onclick")==="%s")'
            '{all[i].dispatchEvent(new MouseEvent("click",{bubbles:true}));'
            'return "clicked";}}'
            'return "MISSING";})()' % expression)


def click_prefix(prefix):
    """press the FIRST element whose click expression starts with
    `prefix` -- used for a file box whose path the rig does not want to
    hard-code."""
    return ('(function(){'
            'var all=document.querySelectorAll("[data-python-onclick]");'
            'for(var i=0;i<all.length;i++){'
            'var v=all[i].getAttribute("data-python-onclick");'
            'if(v.indexOf("%s")===0){'
            'all[i].dispatchEvent(new MouseEvent("click",{bubbles:true}));'
            'return v;}}'
            'return "MISSING";})()' % prefix)


def click_holding(piece):
    """press the FIRST element whose click expression CONTAINS `piece`.

    A probe chip and a variant chip carry whatever file is currently held
    as their middle argument, so a prefix match on `ouro_cov('go',None,`
    finds nothing once a file box has been pressed -- measured, `MISSING`
    on the second pass of this rig.  What identifies these chips is the
    third argument, so that is what is matched.
    """
    return ('(function(){'
            'var all=document.querySelectorAll("[data-python-onclick]");'
            'for(var i=0;i<all.length;i++){'
            'var v=all[i].getAttribute("data-python-onclick");'
            'if(v.indexOf("%s")>=0){'
            'all[i].dispatchEvent(new MouseEvent("click",{bubbles:true}));'
            'return v;}}'
            'return "MISSING";})()' % piece)


def selected_moment():
    return ('(function(){var e=document.querySelector(".momentnow");'
            'return e?e.textContent:"NO CHRONOLOGY ON THE PAGE";})()')


def drawing_census():
    """what the page itself says it drew, read back off the rendered
    SVG -- so a figure is verified, not assumed."""
    return ('(function(){'
            'var svg=document.querySelectorAll("svg.dg");'
            'var boxes=document.querySelectorAll("svg.dg rect.dg-box");'
            'var edges=document.querySelectorAll("svg.dg path.dg-edge");'
            'var arrows=document.querySelectorAll("svg.dg path.dg-arrow");'
            'var heads=document.querySelectorAll(".dg-fig h3");'
            'var names=[];for(var i=0;i<heads.length;i++)'
            'names.push(heads[i].textContent.slice(0,60));'
            'var scripts=document.querySelectorAll("script");'
            'return JSON.stringify({figures:svg.length,boxes:boxes.length,'
            'edges:edges.length,arrows:arrows.length,headings:names,'
            'script_tags_in_the_page:scripts.length});})()')


def scroll_to(fraction):
    """put the page at a fraction of its own height, so a figure below
    the fold is photographed rather than described."""
    return ('(function(){var h=document.body.scrollHeight;'
            'window.scrollTo(0,h*%s);return "scrolled to "+Math.round(h*%s)'
            '+" of "+h;})()' % (fraction, fraction))


def first_commit_tick():
    """press the EARLIEST commit tick the chronology's window is over.

    The commit row draws a windowful at a time (a printed ceiling of 60
    out of every commit), so a commit outside the window has no tick to
    press -- which is what the first pass of this rig hit, `MISSING`, on
    a commit identity taken straight from `git log`.  The day row is
    pressed first to move the window, and then this takes whatever
    commit the window now begins on.  Nothing here chooses a commit by
    what its message says: it takes the first one version control put
    there.
    """
    return ('(function(){'
            'var all=document.querySelectorAll('
            '".scale .tick:not(.day):not(.page)");'
            'if(!all.length)return "NO COMMIT TICKS";'
            'var v=all[0].getAttribute("data-python-onclick");'
            'all[0].dispatchEvent(new MouseEvent("click",{bubbles:true}));'
            'return v;})()')


def earlier_day():
    """a DAY from this repository's own history, one before the newest.

    A day is version control's own mark -- the commits' timestamps
    truncated -- and pressing it moves the chronology's window and
    selects nothing, which is exactly what this rig wants before it
    presses a commit.
    """
    if len(sys.argv) > 1:
        return sys.argv[1]
    root = os.path.expanduser("~/Programming/PseudoCoupHQ")
    out = subprocess.run(
        ["git", "-C", root, "log", "--format=%cI"],
        capture_output=True, text=True).stdout.splitlines()
    days = []
    for line in out:
        day = line.strip()[:10]
        if day and day not in days:
            days.append(day)
    return days[1] if len(days) > 1 else (days[0] if days else None)


EARLIER_DAY = earlier_day()

STEPS = [
    ("click", click("ouro_pane(4)")),
    ("moment", selected_moment()),
    ("census", drawing_census()),
    ("shot", "01_pane4_go_now_figure1_structure"),
    ("scroll", scroll_to(0.36)),
    ("shot", "02_pane4_go_now_figure2_dynamic"),
    ("scroll", scroll_to(0.70)),
    ("shot", "03_pane4_go_now_figure3_direction"),
    ("scroll", scroll_to(0.0)),

    ("click", click_prefix("ouro_cov('go','src/cmd/compile/internal/ssa/")),
    ("census", drawing_census()),
    ("shot", "04_pane4_go_one_file_held_figure1"),
    ("scroll", scroll_to(0.36)),
    ("shot", "05_pane4_go_one_file_held_figure2"),
    ("scroll", scroll_to(0.0)),

    ("click", click_holding("'probe:op_")),
    ("census", drawing_census()),
    ("scroll", scroll_to(0.70)),
    ("shot", "06_pane4_go_one_probe_walk"),
    ("scroll", scroll_to(0.0)),

    ("click", click_holding("'variant:var_")),
    ("census", drawing_census()),
    ("scroll", scroll_to(0.70)),
    ("shot", "07_pane4_go_one_variant"),
    ("scroll", scroll_to(0.0)),

    ("click", click("ouro_cov('cpp',None,None)")),
    ("census", drawing_census()),
    ("shot", "08_pane4_cpp_now_figure1_structure"),
    ("scroll", scroll_to(0.34)),
    ("shot", "09_pane4_cpp_now_figure2_dynamic"),
    ("scroll", scroll_to(0.68)),
    ("shot", "10_pane4_cpp_now_figure3_direction"),
    ("scroll", scroll_to(0.0)),

    ("click", click("ouro_cov('rust',None,None)")),
    ("census", drawing_census()),
    ("shot", "11_pane4_rust_graph_but_no_probe_traces"),
    ("scroll", scroll_to(0.75)),
    ("shot", "12_pane4_rust_the_refusals_named"),
    ("scroll", scroll_to(0.0)),

    # A SECOND MOMENT WHERE THE DRAWING STILL RENDERS: three steps back
    # through the repository's own history.  `prev` is version control's
    # own order and reads no message.
    ("click", click("ouro_moment('prev')")),
    ("click", click("ouro_moment('prev')")),
    ("click", click("ouro_moment('prev')")),
    ("moment", selected_moment()),
    # the compiler chooser has to be pressed again here: a moment change
    # redraws the pane with the arguments it already held, which were
    # rust's.  That is the controller behaving correctly -- the moment is
    # the page's and the pane's own selection is the pane's.
    ("click", click("ouro_cov('go',None,None)")),
    ("census", drawing_census()),
    ("shot", "13_pane4_go_at_an_earlier_commit"),
    ("click", click("ouro_cov('cpp',None,None)")),
    ("census", drawing_census()),
    ("shot", "14_pane4_cpp_at_an_earlier_commit"),

    # A MOMENT WHERE IT CANNOT BE RECOMPUTED, so the refusal is
    # photographed too: an earlier day, where the file-level summary the
    # figures are drawn from was not yet tracked.
    ("window", click("ouro_window('%s')" % (EARLIER_DAY or "now"))),
    ("click", first_commit_tick()),
    ("moment", selected_moment()),
    ("census", drawing_census()),
    ("shot", "15_pane4_at_a_moment_it_cannot_be_recomputed"),

    ("click", click("ouro_moment('now')")),
    ("moment", selected_moment()),
    ("shot", "16_pane4_back_at_now"),
]


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def run():
    os.makedirs(SHOTS, exist_ok=True)
    print("[rig] the earlier DAY this rig moves the window to: %s"
          % EARLIER_DAY)
    app = QApplication(sys.argv[:1])
    window = browser_engine.OurobrowserWindow(start_page="/" + PAGE)
    window.resize(1500, 1100)
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
            QTimer.singleShot(500, advance)
        else:
            def answered(value, kind=kind):
                print("[rig] %s -> %s" % (kind, value))
                QTimer.singleShot(
                    3000 if kind in ("click", "window") else 400, advance)
            window.browser.page().runJavaScript(payload, answered)

    def loaded(ok):
        print("[rig] loadFinished ok=%s" % ok)
        QTimer.singleShot(2500, advance)

    window.browser.loadFinished.connect(loaded)
    window.browser.setUrl(QUrl("ourobrowser://local//" + PAGE))
    app.exec()


if __name__ == "__main__":
    run()
