#!/usr/bin/env python3
"""t98_ouro_shots.py -- drive the REAL Ourobrowser over the dashboard and
photograph PANE 5, STATS, with its explanations.  TASK 98.

This is the ONE thing in task 98 that is not an Airlock lane: the browser
IS the viewer of the deliverable, so looking at the deliverable happens on
the host.  It computes nothing the page does not compute for itself.

It imports `PUBLIC/Ourobrowser/browser_engine.py` and does not edit
it: the engine belongs to the owner and that work is paused.

WHAT IT PHOTOGRAPHS, and why each shot exists
---------------------------------------------
  * pane 5 at the present moment, its first half -- the rows read from a
    stored summary, each carrying its own `?`;
  * ONE EXPLANATION OPENED on a stored row, so the four parts of an
    explanation are on screen: what is counted, out of what, where the
    number comes from, and what it does not mean;
  * the second half -- the rows COUNTED AT RENDER TIME: the corpus by
    language and arrival population, the proof outcome, the arch-opcode
    count distribution, how far machine code repeats, the empty bodies,
    and the term store's states;
  * ONE EXPLANATION OPENED on a computed row, which is the same control
    saying the number was counted rather than read;
  * pane 5 AT A PAST COMMIT, drawing that commit's own numbers;
  * pane 5 at a moment it CANNOT be recomputed, drawing its refusal.

WHAT IT READS BACK, so a claim about the page is measured rather than
described: how many `?` controls the page drew, how many rows went
UNEXPLAINED, how many `<script>` tags the page carries of its own, and
which row each opened explanation sits on.

usage:
    cd PUBLIC/Ourobrowser && \
    LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1 \
    python3 PRIVATE/PseudoCoupHQ/Research/op_pipeline/t98_ouro_shots.py
"""

import os
import resource
import subprocess
import sys

OURO = os.path.expanduser("PUBLIC/Ourobrowser")
PAGE = os.path.expanduser(
    "PRIVATE/PseudoCoupHQ/Research/op_pipeline/dashboard_ouro.html")
SHOTS = os.path.expanduser(
    "PRIVATE/PseudoCoupHQ/DevComms/screens/log_203")

sys.path.insert(0, OURO)

from PyQt6.QtCore import QTimer, QUrl                       # noqa: E402
from PyQt6.QtWidgets import QApplication                    # noqa: E402

import browser_engine                                       # noqa: E402


def click(expression):
    """press the element whose click wire form is `expression`.

    PORT of the same helper in `t93_ouro_shots.py`, unchanged in
    substance: the wire form is the `data-python-onclick` attribute the
    engine rewrites `onclick="python:…"` into, and the attribute values
    are walked and compared rather than spliced into a CSS selector,
    because every one of these expressions carries apostrophes.
    """
    return ('(function(){'
            'var all=document.querySelectorAll("[data-python-onclick]");'
            'for(var i=0;i<all.length;i++){'
            'if(all[i].getAttribute("data-python-onclick")==="%s")'
            '{all[i].dispatchEvent(new MouseEvent("click",{bubbles:true}));'
            'return "clicked";}}'
            'return "MISSING";})()' % expression)


def selected_moment():
    return ('(function(){var e=document.querySelector(".momentnow");'
            'return e?e.textContent:"NO CHRONOLOGY ON THE PAGE";})()')


def stats_census():
    """WHAT THE PAGE ITSELF SAYS IT DREW, read back off the rendered
    document, so every claim about pane 5 is measured.

    `script_tags_in_the_page` counts EVERY script tag the document
    carries, the engine's own two included: the python page contributes
    none, and the `?` control is a `<details>` element, which adds none.
    """
    return ('(function(){'
            'var why=document.querySelectorAll("details.why");'
            'var open=document.querySelectorAll("details.why[open]");'
            'var un=document.querySelectorAll(".unexplained");'
            'var tables=document.querySelectorAll("#pane table");'
            'var rows=document.querySelectorAll("#pane tbody tr");'
            'var gaps=document.querySelectorAll("#pane .gap");'
            'var halves=document.querySelectorAll("#pane h2.half");'
            'var names=[];for(var i=0;i<halves.length;i++)'
            'names.push(halves[i].textContent);'
            'var heads=document.querySelectorAll("#pane h3");'
            'var titles=[];for(var j=0;j<heads.length;j++)'
            'titles.push(heads[j].textContent.slice(0,70));'
            'var scripts=document.querySelectorAll("script");'
            'return JSON.stringify({question_marks:why.length,'
            'opened:open.length,unexplained:un.length,tables:tables.length,'
            'data_rows:rows.length,gap_lines:gaps.length,halves:names,'
            'headings:titles,script_tags_in_the_page:scripts.length});})()')


def open_explanation(which):
    """OPEN one `?`, by its position among the controls the page drew.

    `summary.click()` is called rather than a MouseEvent dispatched: the
    toggle of a `<details>` element is the summary's own default
    activation behaviour, and `HTMLElement.click()` runs it. The row the
    control sits on is read back so the shot's caption is the page's own
    words rather than the rig's.
    """
    return ('(function(){'
            'var all=document.querySelectorAll("details.why");'
            'if(%d>=all.length)return "MISSING -- only "+all.length;'
            'var d=all[%d];'
            'var s=d.querySelector("summary");'
            's.click();'
            'var tr=d.closest("tr");'
            'if(tr)tr.scrollIntoView({block:"center"});'
            'return JSON.stringify({opened:d.open,'
            'row:tr?tr.cells[0].textContent.slice(0,60):"(no row)",'
            'words:d.textContent.replace(/\\s+/g," ").slice(0,120)});})()'
            % (which, which))


def close_all():
    return ('(function(){'
            'var all=document.querySelectorAll("details.why[open]");'
            'for(var i=0;i<all.length;i++)all[i].open=false;'
            'window.scrollTo(0,0);'
            'return "closed "+all.length;})()')


def find_explanation(piece):
    """OPEN the first `?` whose row's first cell contains `piece`."""
    return ('(function(){'
            'var all=document.querySelectorAll("details.why");'
            'for(var i=0;i<all.length;i++){'
            'var tr=all[i].closest("tr");'
            'if(!tr)continue;'
            'if(tr.cells[0].textContent.indexOf("%s")<0)continue;'
            'all[i].querySelector("summary").click();'
            'tr.scrollIntoView({block:"center"});'
            'return JSON.stringify({at:i,open:all[i].open,'
            'row:tr.cells[0].textContent.slice(0,60)});}'
            'return "MISSING";})()' % piece)


def scroll_to(fraction):
    return ('(function(){var h=document.body.scrollHeight;'
            'window.scrollTo(0,h*%s);return "scrolled to "+Math.round(h*%s)'
            '+" of "+h;})()' % (fraction, fraction))


def first_commit_tick():
    """press the EARLIEST commit tick the chronology's window is over.

    PORT of the same helper in `t93_ouro_shots.py`. Nothing here chooses
    a commit by what its message says: it takes the first one version
    control put there.
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
    selects nothing.
    """
    if len(sys.argv) > 1:
        return sys.argv[1]
    days = every_day()
    return days[1] if len(days) > 1 else (days[0] if days else None)


def every_day():
    root = os.path.expanduser("PRIVATE/PseudoCoupHQ")
    out = subprocess.run(
        ["git", "-C", root, "log", "--format=%cI"],
        capture_output=True, text=True).stdout.splitlines()
    days = []
    for line in out:
        day = line.strip()[:10]
        if day and day not in days:
            days.append(day)
    return days


def earliest_day():
    """THE FIRST DAY this repository has, which is where pane 5 has
    nothing to read and nothing to count, so its refusal is drawn.

    A day is version control's own mark and nothing curates it: this
    takes the last day `git log` lists, which is the earliest commit's
    own timestamp.
    """
    days = every_day()
    return days[-1] if days else None


EARLIER_DAY = earlier_day()
EARLIEST_DAY = earliest_day()

STEPS = [
    # THE FIRST PAINT, before anything is pressed.  Read first because
    # the first pass of this rig reported ONE `?` already open on arrival
    # and nothing in the rig had pressed one; this census is where that
    # is measured rather than guessed at.
    ("census", stats_census()),
    # pane 5 is the first paint; pressing its own tab proves the tab works
    ("click", click("ouro_pane(5)")),
    ("moment", selected_moment()),
    ("census", stats_census()),
    ("shot", "01_pane5_stats_the_stored_half"),

    ("explain", find_explanation("members")),
    ("census", stats_census()),
    ("shot", "02_pane5_one_explanation_opened_on_a_stored_row"),
    ("reset", close_all()),

    ("scroll", scroll_to(0.30)),
    ("shot", "03_pane5_the_computed_half_corpus_by_language"),
    ("scroll", scroll_to(0.45)),
    ("shot", "04_pane5_the_arch_opcode_count_distribution"),
    ("scroll", scroll_to(0.78)),
    ("shot", "05_pane5_distinct_machine_code_and_empty_bodies"),
    ("scroll", scroll_to(0.92)),
    ("shot", "06_pane5_the_term_store_counted_here"),
    ("reset", close_all()),

    ("explain", find_explanation("distinct bodies, counted once")),
    ("census", stats_census()),
    ("shot", "07_pane5_one_explanation_opened_on_a_computed_row"),
    ("reset", close_all()),

    ("explain", find_explanation("proved units with no record")),
    ("shot", "08_pane5_the_explanation_that_says_what_a_row_is_not"),
    ("reset", close_all()),

    # A PAST COMMIT, where the pane draws that commit's own numbers.
    ("click", click("ouro_moment('prev')")),
    ("click", click("ouro_moment('prev')")),
    ("click", click("ouro_moment('prev')")),
    ("moment", selected_moment()),
    ("census", stats_census()),
    ("shot", "09_pane5_at_a_past_commit"),
    ("scroll", scroll_to(0.45)),
    ("shot", "10_pane5_at_a_past_commit_the_computed_half"),
    ("reset", close_all()),

    # AN EARLIER DAY STILL, where the artifacts are there but a store is
    # part-built -- the moment where a number moves for a reason that is
    # about version control and not about the research.
    ("window", click("ouro_window('%s')" % (EARLIER_DAY or "now"))),
    ("click", first_commit_tick()),
    ("moment", selected_moment()),
    ("census", stats_census()),
    ("shot", "11_pane5_at_an_earlier_day_a_part_built_store"),

    # A MOMENT IT CANNOT BE RECOMPUTED AT ALL, so the refusal is
    # photographed: the first day this repository has.
    ("window", click("ouro_window('%s')" % (EARLIEST_DAY or "now"))),
    ("click", first_commit_tick()),
    ("moment", selected_moment()),
    ("census", stats_census()),
    ("shot", "12_pane5_at_a_moment_it_cannot_be_recomputed"),

    ("click", click("ouro_moment('now')")),
    ("moment", selected_moment()),
    ("census", stats_census()),
    ("shot", "13_pane5_back_at_now"),
]


#: THE COMPARABLE PASS.  Task 85 and task 86 measured "the real
#: Ourobrowser" by driving the page through twelve screenshots and four
#: moment changes ACROSS ALL FIVE PANES, and reported 577.8 MB and 566.4
#: MB.  Photographing pane 5 alone is a different and smaller pass, so it
#: cannot be set against those numbers.  This pass is shaped like theirs
#: -- every pane, then four moment changes with every pane drawn again --
#: so the figure it reports is comparable to the figure it is compared
#: with.  Run it with `wide` on the command line.
WIDE_STEPS = [
    ("census", stats_census()),
    ("click", click("ouro_pane(1)")),
    ("shot", "w01_pane1"),
    ("click", click("ouro_pane(2)")),
    ("shot", "w02_pane2"),
    ("click", click("ouro_pane(3)")),
    ("shot", "w03_pane3"),
    ("click", click("ouro_pane(4)")),
    ("shot", "w04_pane4"),
    ("click", click("ouro_pane(5)")),
    ("shot", "w05_pane5"),
    ("click", click("ouro_moment('prev')")),
    ("moment", selected_moment()),
    ("shot", "w06_pane5_one_moment_back"),
    ("click", click("ouro_pane(2)")),
    ("shot", "w07_pane2_at_that_moment"),
    ("click", click("ouro_moment('prev')")),
    ("click", click("ouro_pane(3)")),
    ("shot", "w08_pane3_two_moments_back"),
    ("click", click("ouro_moment('prev')")),
    ("click", click("ouro_pane(4)")),
    ("shot", "w09_pane4_three_moments_back"),
    ("click", click("ouro_moment('prev')")),
    ("click", click("ouro_pane(5)")),
    ("census", stats_census()),
    ("shot", "w10_pane5_four_moments_back"),
    ("click", click("ouro_moment('now')")),
    ("click", click("ouro_pane(1)")),
    ("shot", "w11_pane1_back_at_now"),
    ("click", click("ouro_pane(5)")),
    ("census", stats_census()),
    ("shot", "w12_pane5_back_at_now"),
]


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def tree_peak_mb():
    """the resident size of the WHOLE Ourobrowser process tree right now
    -- this process and every process it started, which is where the
    engine's own renderer lives.  Printed beside `peak_mb`, which is this
    process's own high-water mark, because the two answer different
    questions and neither alone is the page's cost."""
    total = 0
    rows = []
    mine = os.getpid()
    listing = subprocess.run(
        ["ps", "-o", "pid=,ppid=,rss=,comm=", "-e"],
        capture_output=True, text=True).stdout.splitlines()
    kin = set([mine])
    grew = True
    while grew:
        grew = False
        for line in listing:
            parts = line.split(None, 3)
            if len(parts) < 4:
                continue
            pid = int(parts[0])
            ppid = int(parts[1])
            if ppid in kin and pid not in kin:
                kin.add(pid)
                grew = True
    for line in listing:
        parts = line.split(None, 3)
        if len(parts) < 4:
            continue
        pid = int(parts[0])
        if pid not in kin:
            continue
        rss = int(parts[2]) / 1024.0
        total = total + rss
        rows.append("%s %.1f MB" % (parts[3].strip(), rss))
    return total, rows


def run():
    os.makedirs(SHOTS, exist_ok=True)
    steps = STEPS
    if "wide" in sys.argv:
        steps = WIDE_STEPS
        print("[rig] THE COMPARABLE PASS: every pane, then four moment "
              "changes with every pane drawn again -- the shape task 85 "
              "and task 86 measured 577.8 MB and 566.4 MB over")
    print("[rig] the earlier DAY this rig moves the window to: %s"
          % EARLIER_DAY)
    app = QApplication(sys.argv[:1])
    window = browser_engine.OurobrowserWindow(start_page="/" + PAGE)
    window.resize(1500, 1100)
    window.show()

    state = {"at": 0, "tree": 0.0, "rows": []}

    def advance():
        if state["at"] >= len(steps):
            print("[rig] peak resident size of the python side: %.1f MB"
                  % peak_mb())
            print("[rig] resident size of the whole process tree at the "
                  "end: %.1f MB" % state["tree"])
            for row in state["rows"]:
                print("[rig]    %s" % row)
            QTimer.singleShot(200, app.quit)
            return
        kind, payload = steps[state["at"]]
        state["at"] += 1
        if kind == "shot":
            total, rows = tree_peak_mb()
            if total > state["tree"]:
                state["tree"] = total
                state["rows"] = rows
            path = os.path.join(SHOTS, payload + ".png")
            image = window.browser.grab()
            saved = image.save(path)
            print("[rig] shot %s -> %s (%dx%d, saved=%s, %d bytes; python "
                  "side %.1f MB, tree %.1f MB)"
                  % (payload, path, image.width(), image.height(), saved,
                     os.path.getsize(path) if os.path.exists(path) else 0,
                     peak_mb(), total))
            QTimer.singleShot(500, advance)
        else:
            def answered(value, kind=kind):
                print("[rig] %s -> %s" % (kind, value))
                QTimer.singleShot(
                    3000 if kind in ("click", "window") else 500, advance)
            window.browser.page().runJavaScript(payload, answered)

    def loaded(ok):
        print("[rig] loadFinished ok=%s" % ok)
        QTimer.singleShot(3000, advance)

    window.browser.loadFinished.connect(loaded)
    window.browser.setUrl(QUrl("ourobrowser://local//" + PAGE))
    app.exec()


if __name__ == "__main__":
    run()
