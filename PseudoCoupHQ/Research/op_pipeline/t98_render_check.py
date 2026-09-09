#!/usr/bin/env python3
"""t98_render_check.py -- pane 5, rendered off the page and checked.

WHAT IT PROVES, each thing with its own printed line:

  1. EVERY ROW CARRIES AN EXPLANATION.  The renderer draws an
     `unexplained` marker in place of a `?` wherever a row's key has no
     record in `dashboard_stats.MEANINGS`.  This program counts those
     markers in the rendered html and prints the count with the number of
     `?` controls beside it.  A row that went without one is therefore a
     number on this page, not something a reader has to notice.
  2. NO JAVASCRIPT.  It counts `<script` in what the pane emits.  The
     `?` is a `<details>` element and adds none.
  3. THE FIGURES.  It prints every computed figure off the same walk the
     pane runs, so each can be set against the figures the task brief
     measured.
  4. THE COST.  Wall clock and peak resident size for one render, against
     the page's stated cap of 1,500 MB.
  5. THE PAST.  It renders pane 5 at a run of past moments and reports,
     per moment, whether the pane drew numbers or drew its refusal.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

This program groups nothing and pairs nothing.  It renders a pane and
counts markers in the html.

usage:
    t98_render_check.py now         render pane 5 at the present moment
    t98_render_check.py figures     the computed figures, printed
    t98_render_check.py past N      pane 5 at N past moments
    t98_render_check.py all
"""

import os
import re
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dashboard_ouro as page                                   # noqa: E402
import dashboard_stats as statspane                             # noqa: E402


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def render_now():
    started = time.time()
    markup = page.render(5)
    seconds = time.time() - started

    controls = markup.count('class="whymark"')
    unexplained = markup.count('class="unexplained"')
    scripts = markup.count("<script")
    tables = markup.count("<table")
    rows = markup.count("<tr>")
    headers = markup.count("<thead>")

    say("== pane 5 rendered at the present moment")
    say("wall clock                          %.2f s" % seconds)
    say("peak resident size                  %.1f MB (cap %d MB)"
        % (peak_mb(), page.MEMORY_CAP_MB))
    say("bytes of html                       %d" % len(markup))
    say("tables                              %d" % tables)
    say("data rows (every <tr> less headers) %d" % (rows - headers))
    say("`?` controls drawn                  %d" % controls)
    say("rows drawn as UNEXPLAINED           %d" % unexplained)
    say("occurrences of `<script`            %d" % scripts)
    say("explanation records on file         %d" % len(statspane.MEANINGS))
    if unexplained:
        say("")
        say("THE UNEXPLAINED ROWS, with the key each one names:")
        for match in re.finditer(
                r'<span class="unexplained" title="the row key is ([^"]*)"',
                markup):
            say("   %s" % match.group(1))
    used = set(re.findall(r'title="the row key is ([^"]*)"', markup))
    say("")
    say("explanation records never used by any row drawn now:")
    drawn = set()
    for key in statspane.MEANINGS:
        drawn.add(key)
    unused = sorted(drawn - set(used))
    return markup


def figures():
    started = time.time()
    moment = page.current_moment()
    found = statspane.corpus_analysis(moment, page.guard_memory,
                                      page.OP_DIR)
    terms = statspane.term_store_analysis(moment, page.guard_memory,
                                          page.OP_DIR)
    say("== the computed figures, off the same walk the pane runs")
    say("canonical-form generation           canon%s over %d documents"
        % (found["generation"], found["inputs"]))
    say("units in the corpus                 %d" % found["units"])
    say("languages                           %d" % len(found["by_lang"]))
    say("units the gate proved               %d" % found["proved"])
    say("units the gate did not prove        %d"
        % (found["units"] - found["proved"]))
    say("-- per language")
    for lang in sorted(found["by_lang"]):
        say("   %-10s %d" % (lang, found["by_lang"][lang]))
    say("-- per arrival population")
    for population in sorted(found["by_pop"]):
        say("   %-14s %d" % (population, found["by_pop"][population]))
    say("-- every outcome value")
    for outcome in sorted(found["outcomes"]):
        say("   %-30s %d" % (outcome, found["outcomes"][outcome]))
    say("-- the arch-opcode count distribution, its shape")
    for population in sorted(found["opcode_spread"]):
        shape = found["opcode_spread"][population]
        say("   %-14s units %d, distinct opcodes %d, peak %d (%d, %.1f%%), "
            "median %d, longest %d, empty %d"
            % (population, shape["population"],
               found["vocabulary"][population], shape["peak"],
               shape["peak_units"], shape["peak_share"], shape["median"],
               shape["largest"], shape["zero"]))
    say("-- machine code repetition")
    say("   units carrying machine code        %d" % found["compiled"])
    say("   distinct bodies, corpus-wide       %d"
        % found["distinct_corpus_wide"])
    say("   distinct bodies, summed per lang   %d"
        % found["distinct_summed_per_language"])
    say("   bodies in more than one language   %d"
        % found["bodies_in_more_than_one_language"])
    say("   units per distinct, corpus-wide    %.1f"
        % (found["compiled"] / float(found["distinct_corpus_wide"])))
    say("   units per distinct, summed         %.1f"
        % (found["compiled"]
           / float(found["distinct_summed_per_language"])))
    say("   most repeated body                 %d units, bytes %s, "
        "languages %s"
        % (found["most_repeated"], found["most_repeated_bytes"],
           ", ".join(found["most_repeated_languages"])))
    say("   per language: units / distinct / ratio")
    for lang in sorted(found["distinct_by_lang"]):
        units = found["compiled_by_lang"][lang]
        distinct = found["distinct_by_lang"][lang]
        say("     %-10s %d / %d / %.1f"
            % (lang, units, distinct, units / float(distinct)))
    say("-- empty bodies")
    for population in sorted(found["empty_bodies"]):
        say("   %-14s %d" % (population, found["empty_bodies"][population]))
    say("-- the term store")
    say("   store                              %s, %d shards"
        % (terms["store"], terms["shards"]))
    say("   records                            %d" % terms["records"])
    say("   proved units with no record        %d"
        % (found["proved"] - terms["records"]))
    for state in sorted(terms["by_state"]):
        say("   %-34s %d" % (state, terms["by_state"][state]))
    say("   per language: records / by state")
    for lang in sorted(terms["by_lang"]):
        parts = []
        for state in sorted(terms["by_state"]):
            parts.append("%s %d"
                         % (state,
                            terms["by_lang_state"].get((lang, state), 0)))
        say("     %-10s %d   (%s)"
            % (lang, terms["by_lang"][lang], ", ".join(parts)))
    say("")
    say("figures: %.2f s, peak resident %.1f MB"
        % (time.time() - started, peak_mb()))


def past(count):
    order = page.moments()
    total = len(order)
    step = max(1, total // count)
    picked = []
    at = 0
    while at < total and len(picked) < count:
        picked.append(order[at])
        at = at + step
    picked.append(order[-1])

    say("== pane 5 at %d moments of %d, refusals and numbers"
        % (len(picked), total))
    drew = 0
    refused = 0
    errors = 0
    for one in picked:
        page.set_moment(one.key)
        markup = page.render(5)
        controls = markup.count('class="whymark"')
        unexplained = markup.count('class="unexplained"')
        state = "numbers"
        if "not recomputable at this moment" in markup:
            state = "REFUSED"
            refused = refused + 1
        elif "<h2>error</h2>" in markup:
            state = "ERROR"
            errors = errors + 1
        else:
            drew = drew + 1
        say("   %-30s %-9s %4d `?`, %d unexplained, %d gap lines, "
            "%d bytes"
            % (one.label(), state, controls, unexplained,
               markup.count('class="gap"'), len(markup)))
    page.set_moment("now")
    say("")
    say("moments drawing numbers %d, drawing a refusal %d, in error %d"
        % (drew, refused, errors))
    say("peak resident over the whole pass %.1f MB (cap %d MB)"
        % (peak_mb(), page.MEMORY_CAP_MB))


def keys(count):
    """WHICH row keys go unexplained, and at which moment.

    The renderer names the missing key inside the `unexplained` marker it
    draws, so this reads them back out of the html rather than guessing.
    A key appearing only at a past moment is an EARLIER GENERATION of an
    artifact carrying a summary field the present generation dropped --
    which is exactly the case the marker exists for.
    """
    order = page.moments()
    total = len(order)
    step = max(1, total // count)
    picked = []
    at = 0
    while at < total and len(picked) < count:
        picked.append(order[at])
        at = at + step
    picked.append(order[-1])

    say("== every row key drawn as UNEXPLAINED, and where")
    seen = {}
    for one in picked:
        page.set_moment(one.key)
        markup = page.render(5)
        found = re.findall(
            r'<span class="unexplained" title="the row key is ([^"]*)"',
            markup)
        for key in sorted(set(found)):
            if key not in seen:
                seen[key] = []
            seen[key].append(one.label())
        if found:
            say("   %-30s %s" % (one.label(), ", ".join(sorted(set(found)))))
    page.set_moment("now")
    say("")
    if not seen:
        say("no row key went unexplained at any of the %d moments walked"
            % len(picked))
    for key in sorted(seen):
        say("   %-60s at %d moment(s)" % (key, len(seen[key])))


def split():
    """HOW MANY ROWS ARE IN EACH HALF, cut at the page's own marker.

    The pane draws `<h2 class="half">` twice, once for each half, so the
    split is read off the rendered html at that marker rather than
    counted by hand from a list someone kept.
    """
    markup = page.render(5)
    mark = '<h2 class="half">counted at render time</h2>'
    at = markup.find(mark)
    if at < 0:
        say("THE MARKER IS NOT ON THE PAGE -- the halves cannot be counted")
        return
    stored = markup[:at]
    computed = markup[at:]

    def rows_in(part):
        return part.count("<tr>") - part.count("<thead>")

    say("== pane 5's rows, split at the page's own half marker")
    say("rows read from a stored summary  %d" % rows_in(stored))
    say("rows counted at render time      %d" % rows_in(computed))
    say("rows in total                    %d" % rows_in(markup))
    say("tables in the stored half        %d" % stored.count("<table"))
    say("tables in the computed half      %d" % computed.count("<table"))
    say("`?` controls, stored half        %d"
        % stored.count('class="whymark"'))
    say("`?` controls, computed half      %d"
        % computed.count('class="whymark"'))
    say("unexplained rows, either half    %d"
        % markup.count('class="unexplained"'))


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which == "split":
        split()
        return
    if which == "keys":
        count = 14
        if len(sys.argv) > 2:
            count = int(sys.argv[2])
        keys(count)
        say("")
        say("whole process peak resident %.1f MB" % peak_mb())
        return
    if which in ("now", "all"):
        render_now()
        say("")
    if which in ("figures", "all"):
        figures()
        say("")
    if which in ("past", "all"):
        count = 12
        if len(sys.argv) > 2:
            count = int(sys.argv[2])
        past(count)
        say("")
    say("whole process peak resident %.1f MB" % peak_mb())


if __name__ == "__main__":
    main()
