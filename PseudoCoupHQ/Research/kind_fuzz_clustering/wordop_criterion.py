#!/usr/bin/env python3
"""wordop_criterion.py -- decision 43 folded: leg G and leg R joined
into one admitted/library table over all twelve languages.

Leg G is wordop_survey.json (the grammar's own declarations).
Leg R is raw/lr_words*.txt (the reservation probes).

A leg-R verdict is READABLE only if the pass that produced it also
produced an ACCEPT for its CONTROL word `zzfoo`, which is an ordinary
identifier in every one of the twelve.  A pass whose control REFUSES is
measuring its own harness and its verdicts are dropped, not read.  Two
passes did exactly that and were re-run; both re-runs are folded here
and the later pass wins.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LANGS = ["go","rust","cpp","swift","dart","csharp","kotlin","java",
         "typescript","python","ruby","php"]
CONTROL = "zzfoo"


def read_legR():
    passes = sorted(f for f in os.listdir(RAW)
                    if re.match(r"^lr_words\d*\.txt$", f))
    order = sorted(passes, key=lambda f: (len(f), f))
    per_pass = []
    for f in order:
        tab = {}
        for line in open(os.path.join(RAW, f)):
            p = line.strip().split("|")
            if len(p) == 3:
                tab.setdefault(p[0], {})[p[1]] = p[2]
        per_pass.append((f, tab))
    verdict, provenance, unreadable = {}, {}, []
    for f, tab in per_pass:
        for L, ws in tab.items():
            if ws.get(CONTROL) != "ACCEPT":
                for w in ws:
                    if w != CONTROL:
                        unreadable.append(dict(pass_=f, language=L, word=w,
                                               control=ws.get(CONTROL, "absent")))
                continue
            for w, v in ws.items():
                if w == CONTROL:
                    continue
                verdict[(L, w)] = v
                provenance[(L, w)] = f
    return verdict, provenance, unreadable, [f for f, _ in per_pass]


def main():
    G = json.load(open(os.path.join(HERE, "wordop_survey.json")))
    R, prov, unread, passes = read_legR()
    rows, admitted = [], {L: [] for L in LANGS}
    library = {L: [] for L in LANGS}
    words = sorted({w for (L, w) in R} |
                   {w for L in LANGS for w in G[L]["grammar_declared_words"]})
    for L in LANGS:
        g = set(G[L]["grammar_declared_words"])
        for w in sorted(g | {w for (l, w) in R if l == L}):
            legg = "yes" if w in g else "no"
            # a MULTI-WORD spelling ("is not", "not in") is reserved
            # iff every word in it is reserved on its own.
            parts = w.split()
            if len(parts) > 1:
                vs = [R.get((L, q)) for q in parts]
                legr = ("REFUSE" if all(v == "REFUSE" for v in vs)
                        else ("ACCEPT" if any(v == "ACCEPT" for v in vs)
                              else None))
            else:
                legr = R.get((L, w))
            legr = legr or "unread"
            legrs = {"REFUSE": "yes", "ACCEPT": "no"}.get(legr, "unread")
            if legg == "yes" and legrs == "yes":
                verdict = "ADMIT"; admitted[L].append(w)
            elif legrs == "unread":
                verdict = "UNREAD"
            else:
                verdict = "library"; library[L].append(w)
            rows.append(dict(language=L, word=w, leg_G=legg, leg_R=legrs,
                             leg_R_raw=legr, verdict=verdict,
                             source=prov.get((L, w))))
    out = dict(decision=43, legs=dict(
        G="grammar declares the word in the operator slot of a "
          "binary-shaped expression node (wordop_survey.py)",
        R="the language's own checker REFUSES an ordinary variable named "
          "with the word (lanes lr_words*.sh)"),
        control_word=CONTROL, passes=passes,
        rows=rows, admitted=admitted, library=library,
        unreadable=unread)
    json.dump(out, open(os.path.join(HERE, "wordop_criterion.json"), "w"),
              indent=1)
    print("| language | grammar declares | reserved | admitted | library |")
    print("|---|---|---|---|---|")
    for L in LANGS:
        g = G[L]["grammar_declared_words"]
        res = sorted(w for (l, w) in R if l == L and R[(l, w)] == "REFUSE")
        print("| %s | %s | %s | %s | %s |"
              % (L, ", ".join(g) or "—", ", ".join(res) or "—",
                 ", ".join(admitted[L]) or "—",
                 ", ".join(library[L]) or "—"))
    if unread:
        print("\nDROPPED, control did not accept: %d verdicts" % len(unread))
        for u in unread[:20]:
            print("  %s %s.%s (control %s)"
                  % (u["pass_"], u["language"], u["word"], u["control"]))


if __name__ == "__main__":
    main()
