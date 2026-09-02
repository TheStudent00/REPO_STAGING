#!/usr/bin/env python3
"""build_family_graph.py -- the data behind `family_graph_explorer_v1.html`.

NOTHING STRUCTURAL IS DECIDED HERE.  No threshold is ruled, no name is
coined.  The nodes are the IDENTITY (CONTRACT) families of log_070 read
straight out of `dominant_operators_v1.json`; the connectors are the
disagreement kinds of the classifier the owner ruled on 2026-08-23 (log_069),
re-derived cell by cell from `matrices_full_v2/` by the same rule the
log_070 pipeline uses, so the per-kind totals must reproduce log_070's
table exactly (this script asserts that they do).

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.

The classifier, quoted from `log070_dominant_operators.py`:

    vv = disagreeing cells where BOTH sides answer a value  (VALUE)
    wi = disagreeing cells where exactly one side answers    (WINDOW)
    tt = the rest -- token against a DIFFERENT token         (DECLINE-KIND)

    vv and wi -> MIXED ; vv only -> VALUE ; wi only -> WINDOW ;
    otherwise -> DECLINE-KIND

The settled decline rule ("zero comparable keys means NO connector, not a
zero-weight one", `CLAUDE.md`) splits the WINDOW-only pairs into the ones
that ARE connectors and the ones that are refused; both are emitted, the
refused ones flagged, and only the kept ones ever enter a component.

Output: `family_graph_v1.json`, embedded verbatim into the explorer.
"""

import collections
import csv
import datetime
import hashlib
import json
import os
import sys

import numpy as np

csv.field_size_limit(10 ** 9)

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, "matrices_full_v2")
SRC_JSON = os.path.join(HERE, "dominant_operators_v1.json")
OUT_JSON = os.path.join(HERE, "family_graph_v1.json")
SRC_HTML = os.path.join(HERE, "family_graph_explorer_v1.src.html")
OUT_HTML = os.path.join(HERE, "family_graph_explorer_v1.html")
SEP = ";"
DECLINE_EXACT = {"REFUSE", "ABORT"}
NOT_ASKED = "UNREPRESENTABLE"
CLIQUE_CAP = 400000


def is_value(c):
    return not (c in DECLINE_EXACT or c == NOT_ASKED or c.startswith("RAISE:"))


def out_form(c):
    if c.startswith("[") or c == "nan":
        return "number"
    if c in ("true", "false"):
        return "truth"
    if c == "null":
        return "nothing"
    if c.startswith("t|"):
        return "text"
    if c.startswith("c|"):
        return "container"
    if c.startswith("opaque:"):
        return "opaque"
    return "UNKNOWN-FORM"


def load():
    """byte-for-byte the loader of log070_dominant_operators.py, so the
    per-block family ORDER -- and therefore every `block#i` id -- is the
    same object."""
    idx = json.load(open(os.path.join(FULL, "index.json")))
    grid = idx["grid_sizes"]
    spell_of = {}
    for k, v in idx["matrices"].items():
        spell_of[(v["language"], v["file"].split(".")[1],
                  v["level"])] = v["operator"]
    blocks = collections.defaultdict(lambda: collections.OrderedDict())
    profiles = []
    for fn in sorted(os.listdir(FULL)):
        if not fn.endswith(".csv"):
            continue
        parts = fn[:-4].split(".")
        lang, tok, lvl = parts[0], parts[1], int(parts[2][1:])
        sp = spell_of.get((lang, tok, lvl), tok)
        for r in csv.DictReader(open(os.path.join(FULL, fn))):
            block = (r["form_pair"], int(r["level"]))
            vs = r["output_canon_vector"]
            h = hashlib.blake2b(vs.encode(), digest_size=16).digest()
            slot = blocks[block].setdefault(h, dict(vec=vs, members=[]))
            pid = len(profiles)
            profiles.append(dict(
                idx=pid, lang=lang, sp=sp, level=lvl, block=block,
                lhs=r["lhs_holder"], rhs=r["rhs_holder"],
                win_a=r["src_x_set_a"], win_b=r["src_x_set_b"],
                key="%s.%s %s x %s" % (lang, sp, r["lhs_holder"],
                                       r["rhs_holder"])))
            slot["members"].append(pid)
    return idx, blocks, profiles


def components(n, adj):
    seen, out = set(), []
    for v in range(n):
        if v in seen:
            continue
        stack, comp = [v], []
        seen.add(v)
        while stack:
            u = stack.pop()
            comp.append(u)
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        out.append(sorted(comp))
    return out


def bron_kerbosch(R, P, X, adj, out, cap):
    if len(out) > cap:
        return
    if not P and not X:
        out.append(sorted(R))
        return
    pivot = max(P | X, key=lambda u: len(adj[u] & P))
    for v in list(P - adj[pivot]):
        bron_kerbosch(R | {v}, P & adj[v], X & adj[v], adj, out, cap)
        P = P - {v}
        X = X | {v}
        if len(out) > cap:
            return


def is_clique(comp, adj):
    s = set(comp)
    return all((s - {v}) <= adj[v] for v in comp)


def main():
    sys.setrecursionlimit(100000)
    src = json.load(open(SRC_JSON))
    fam_by_id = {f["id"]: f for f in src["families"]}
    relax_by_block = {r["block"]: r for r in src["relaxation"]}
    stats_by_block = {b["block"]: b for b in src["block_stats"]}

    idx, blocks, profiles = load()
    print("profiles %d   gate blocks %d" % (len(profiles), len(blocks)))

    out_blocks = []
    total = collections.Counter()
    for block in sorted(blocks):
        fp, lvl = block
        bname = "%s/L%d" % (fp, lvl)
        slots = blocks[block]
        hashes = list(slots)
        d = len(hashes)
        cells = slots[hashes[0]]["vec"].count(SEP) + 1

        codes = np.zeros((d, cells), dtype=np.int32)
        vmask = np.zeros((d, cells), dtype=bool)
        interned = {}
        sigs = []
        fams = []
        for i, h in enumerate(hashes):
            v = slots[h]["vec"].split(SEP)
            row, mrow = codes[i], vmask[i]
            f = set()
            nv = nd_ = nu = 0
            for p, c in enumerate(v):
                cc = interned.get(c)
                if cc is None:
                    cc = interned[c] = len(interned)
                row[p] = cc
                iv = is_value(c)
                mrow[p] = iv
                if iv:
                    f.add(out_form(c))
                    nv += 1
                elif c == NOT_ASKED:
                    nu += 1
                else:
                    nd_ += 1
            sigs.append(frozenset(f))
            fid = "%s#%d" % (bname, i)
            srcf = fam_by_id[fid]
            mem = [profiles[x] for x in slots[h]["members"]]
            memkeys = sorted(p["key"] for p in mem)
            assert memkeys == sorted(srcf["members"]), (fid, memkeys)
            fams.append(dict(
                id=fid, i=i,
                name=srcf["name"],
                census_name=(srcf["name"] if srcf["name"] not in
                             ("UNCLASSIFIED", "NON-DISCRIMINATING") else None),
                consistent_with=srcf.get("consistent_with", []),
                n_profiles=srcf["n_profiles"],
                members=srcf["members"],
                member_windows=srcf["member_windows"],
                spellings=srcf["spellings"],
                spelling_counts=srcf["spelling_counts"],
                languages=srcf["languages"],
                output_form_signature=srcf["output_form_signature"],
                output_shape_signature=srcf["output_shape_signature"],
                n_cells=srcf["n_cells"],
                n_value_cells=srcf["n_value_cells"],
                n_declines=nd_, n_unrepresentable=nu))
            assert srcf["n_value_cells"] == nv, fid
            assert srcf["n_cells"] == cells, fid

        # ---------------- the classifier, cell by cell ----------------
        E = {k: dict(a=[], b=[], nd=[], vv=[], wi=[], tt=[], cmp=[])
             for k in ("WINDOW", "WINDOW_REFUSED", "VALUE", "DECLINE")}
        MIX = dict(a=[], b=[], nd=[])
        adj = {i: set() for i in range(d)}
        adj_hard = {i: set() for i in range(d)}
        kinds = collections.Counter()
        for i in range(d):
            ci, mi = codes[i], vmask[i]
            for j in range(i + 1, d):
                neq = ci != codes[j]
                nd = int(np.count_nonzero(neq))
                if nd == 0:
                    continue
                mj = vmask[j]
                both = mi & mj
                comparable = int(np.count_nonzero(both))
                vv = int(np.count_nonzero(neq & both))
                wi = int(np.count_nonzero(neq & (mi ^ mj)))
                tt = nd - vv - wi
                if vv and wi:
                    k = "MIXED"
                elif vv:
                    k = "VALUE"
                elif wi:
                    k = "WINDOW"
                else:
                    k = "DECLINE-KIND"
                kinds[k] += 1
                if k == "MIXED":
                    MIX["a"].append(i)
                    MIX["b"].append(j)
                    MIX["nd"].append(nd)
                    continue
                if k == "WINDOW":
                    slot = "WINDOW" if comparable else "WINDOW_REFUSED"
                    if comparable:
                        adj[i].add(j)
                        adj[j].add(i)
                        if sigs[i] == sigs[j]:
                            adj_hard[i].add(j)
                            adj_hard[j].add(i)
                else:
                    slot = "VALUE" if k == "VALUE" else "DECLINE"
                t = E[slot]
                t["a"].append(i)
                t["b"].append(j)
                t["nd"].append(nd)
                t["vv"].append(vv)
                t["wi"].append(wi)
                t["tt"].append(tt)
                t["cmp"].append(comparable)

        comp = components(d, adj)
        comp_hard = components(d, adj_hard)
        big = [c for c in comp if len(c) > 1]
        nonclique = sum(1 for c in big if len(c) > 2 and not is_clique(c, adj))
        cl = []
        bron_kerbosch(set(), set(range(d)), set(), adj, cl, CLIQUE_CAP)

        comp_detail = []
        for c in sorted(big, key=lambda c: -len(c)):
            names = sorted({fams[x]["name"] for x in c})
            cn = sorted({fams[x]["census_name"] for x in c
                         if fams[x]["census_name"]})
            comp_detail.append(dict(
                members=c, size=len(c),
                n_profiles=sum(fams[x]["n_profiles"] for x in c),
                names=names, census_names=cn,
                spans_modes=len(cn) > 1,
                is_clique=is_clique(c, adj),
                spellings=sorted({s for x in c for s in fams[x]["spellings"]}),
                languages=sorted({l for x in c
                                  for l in fams[x]["languages"]})))

        # the log_070 relaxation table must reproduce exactly
        r = relax_by_block[bname]
        s = stats_by_block[bname]
        assert kinds["WINDOW"] == s["WINDOW"], (bname, kinds, s)
        assert kinds["VALUE"] == s["VALUE"], bname
        assert kinds["MIXED"] == s["MIXED"], bname
        assert kinds["DECLINE-KIND"] == s["DECLINE_KIND"], bname
        assert len(E["WINDOW"]["a"]) == r["window_edges"], bname
        assert (len(E["WINDOW_REFUSED"]["a"]) ==
                r["window_edges_refused_no_comparable_cell"]), bname
        assert len(comp) == r["components"], bname
        assert len(cl) == r["maximal_cliques"], bname
        assert len(comp_hard) == r["hard_gate_components"], bname

        for k in kinds:
            total[k] += kinds[k]
        out_blocks.append(dict(
            block=bname, form_pair=fp, level=lvl, cells=cells,
            n_families=d, n_profiles=s["profiles"], pairs=s["pairs"],
            kind_counts=dict(WINDOW=kinds["WINDOW"], VALUE=kinds["VALUE"],
                             MIXED=kinds["MIXED"],
                             DECLINE_KIND=kinds["DECLINE-KIND"]),
            window_edges_kept=len(E["WINDOW"]["a"]),
            window_edges_refused=len(E["WINDOW_REFUSED"]["a"]),
            components=len(comp), components_multi=len(big),
            largest_component=max((len(c) for c in comp), default=0),
            components_not_cliques=nonclique,
            maximal_cliques=len(cl),
            hard_gate_components=len(comp_hard),
            mode_spanning_components=sum(1 for c in comp_detail
                                         if c["spans_modes"]),
            families=fams, edges=E, mixed=MIX,
            component_detail=comp_detail))
        print("  %-24s families=%-5d W=%-6d V=%-6d M=%-7d D=%-4d "
              "comp=%-4d cliques=%d"
              % (bname, d, kinds["WINDOW"], kinds["VALUE"], kinds["MIXED"],
                 kinds["DECLINE-KIND"], len(comp), len(cl)))

    assert total["WINDOW"] == src["pair_kinds"]["WINDOW"]
    assert total["VALUE"] == src["pair_kinds"]["VALUE"]
    assert total["MIXED"] == src["pair_kinds"]["MIXED"]
    assert total["DECLINE-KIND"] == src["pair_kinds"]["DECLINE-KIND"]

    # -------- the two rulings' witnesses, located rather than described
    def find(bname, member):
        b = [x for x in out_blocks if x["block"] == bname][0]
        return [f for f in b["families"] if member in f["members"]][0]

    ww1 = [x for x in out_blocks if x["block"] == "whole|whole/L1"][0]
    chain = [find("whole|whole/L1", "php.+ int x int"),
             find("whole|whole/L1", "csharp.+ short x short"),
             find("whole|whole/L1", "cpp.+ int64_t x int64_t")]
    ci = [f["i"] for f in chain]

    def edge_between(blk, a, b):
        lo, hi = min(a, b), max(a, b)
        for slot in ("WINDOW", "WINDOW_REFUSED", "VALUE", "DECLINE"):
            t = blk["edges"][slot]
            for n in range(len(t["a"])):
                if t["a"][n] == lo and t["b"][n] == hi:
                    return dict(kind=slot, nd=t["nd"][n], vv=t["vv"][n],
                                wi=t["wi"][n], tt=t["tt"][n],
                                comparable=t["cmp"][n])
        m = blk["mixed"]
        for n in range(len(m["a"])):
            if m["a"][n] == lo and m["b"][n] == hi:
                return dict(kind="MIXED", nd=m["nd"][n])
        return None

    hop1 = edge_between(ww1, ci[0], ci[1])
    hop2 = edge_between(ww1, ci[1], ci[2])
    direct = edge_between(ww1, ci[0], ci[2])
    comp_of = None
    for c in ww1["component_detail"]:
        if ci[0] in c["members"]:
            comp_of = c
    witness_16 = dict(
        block="whole|whole/L1",
        families=[dict(id=f["id"], i=f["i"], name=f["name"],
                       member=m) for f, m in zip(chain, [
                           "php.+ int x int", "csharp.+ short x short",
                           "cpp.+ int64_t x int64_t"])],
        hop1=hop1, hop2=hop2, direct=direct,
        component_size=comp_of["size"] if comp_of else None,
        component_profiles=comp_of["n_profiles"] if comp_of else None,
        component_census_names=comp_of["census_names"] if comp_of else None)
    print("\n1.6 chain:", json.dumps(witness_16)[:600])

    w15 = None
    for blk in out_blocks:
        fa = [f for f in blk["families"]
              if "cpp.% int32_t x int32_t" in f["members"]]
        fb = [f for f in blk["families"]
              if "csharp.% int x int" in f["members"]]
        if fa and fb:
            e = edge_between(blk, fa[0]["i"], fb[0]["i"])
            if e and e["kind"] == "DECLINE":
                w15 = dict(block=blk["block"], a=fa[0]["id"], ai=fa[0]["i"],
                           b=fb[0]["id"], bi=fb[0]["i"], edge=e)
                break
    print("1.5 witness:", json.dumps(w15))

    doc = dict(
        built=datetime.datetime.now().isoformat(timespec="seconds"),
        source="Research/kind_fuzz_clustering/matrices_full_v2/ + "
               "dominant_operators_v1.json",
        status="PRELIMINARY -- a picture of measurements; nothing "
               "structural decided, no threshold ruled, no name coined",
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        default_block="whole|whole/L1",
        int_spring=0.0006, ext_spring=0.035,
        n_families=sum(b["n_families"] for b in out_blocks),
        n_profiles=len(profiles),
        pair_kinds=dict(total),
        totals=dict(
            WINDOW=total["WINDOW"], VALUE=total["VALUE"],
            MIXED=total["MIXED"], DECLINE_KIND=total["DECLINE-KIND"],
            window_kept=sum(b["window_edges_kept"] for b in out_blocks),
            window_refused=sum(b["window_edges_refused"] for b in out_blocks),
            components=sum(b["components"] for b in out_blocks),
            maximal_cliques=sum(b["maximal_cliques"] for b in out_blocks)),
        witness_1_6=witness_16, witness_1_5=w15,
        blocks=out_blocks)
    with open(OUT_JSON, "w") as fh:
        json.dump(doc, fh, separators=(",", ":"))
    print("\nwrote %s  %.1f MB" % (OUT_JSON,
                                   os.path.getsize(OUT_JSON) / 1e6))
    emit()


def emit():
    """splice the data into the single self-contained page.  NO CDN, no
    external script, no external URL of any kind."""
    src = open(SRC_HTML).read()
    data = open(OUT_JSON).read()
    assert src.count("__DATA__") == 1
    html = src.replace("__DATA__", data)
    assert "://" not in html.replace(
        "http://www.w3.org", "")   # no URL survives; there are none
    with open(OUT_HTML, "w") as fh:
        fh.write(html)
    print("wrote %s  %.1f MB" % (OUT_HTML, os.path.getsize(OUT_HTML) / 1e6))


if __name__ == "__main__":
    if "--emit-only" in sys.argv:
        emit()
    else:
        main()
