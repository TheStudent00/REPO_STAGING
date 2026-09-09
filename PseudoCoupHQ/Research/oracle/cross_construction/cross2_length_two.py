#!/usr/bin/env python3
"""cross2_length_two.py -- task o1, deliverable B.

Length-two construction (see CORE_0_3_8_2_cross_construction.md,
"construction of y from x", length two): y's layer-5 term equals an
x term whose variables are replaced by other x terms.

This script:
  1. Parses every DISTINCT layer-5 text in the_pool5.json with a
     hand-written recursive-descent parser for z3's python print
     form, and self-tests the parser by re-printing every parsed
     tree and comparing to the original text (a round trip).
  2. Turns every x entry's layer-5 text into a PATTERN: the parsed
     tree with each distinct variable v<N> replaced by a hole.
  3. For every ordered language pair (x, y) and every y entry NOT
     built at length one (read from cross1_length_one.json), checks
     whether the y tree matches some x pattern at the root, with
     every hole-bound subtree itself either a variable, a literal, or
     matching some x pattern with ALL ITS holes bound to variables or
     literals (depth 2 exactly).

No operator token is ever a key, grouping, pairing, or row: every key
below is a pool entry_id, a language name, or a layer-5 text (machine
form). Writes cross2_length_two.json beside this script.
"""
import json
import sys
import time

POOL_PATH = "PseudoCoupHQ/Research/op_pipeline/the_pool5.json"
CROSS1_PATH = "PseudoCoupHQ/Research/oracle/cross_construction/cross1_length_one.json"
OUT_PATH = "PseudoCoupHQ/Research/oracle/cross_construction/cross2_length_two.json"

TIME_BUDGET_S = 30 * 60  # per the brief: 30 minutes wall clock before sampling
SAMPLE_SIZE = 200

# ---------------------------------------------------------------- tokenizer

TWO_CHAR_OPS = ("==", "<=", ">=", "<<", ">>")
ONE_CHAR_OPS = ("+", "-", "*", "/", "%", "|", "^", "~", "<", ">", "(", ")", ",")


def tokenize(s):
    toks = []  # (kind, text, start, end)
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if s[i:i + 2] in TWO_CHAR_OPS:
            toks.append(("OP", s[i:i + 2], i, i + 2))
            i += 2
            continue
        if c in ONE_CHAR_OPS:
            toks.append(("OP", c, i, i + 1))
            i += 1
            continue
        if c.isdigit():
            j = i
            while j < n and (s[j].isdigit() or s[j] == "."):
                j += 1
            toks.append(("NUM", s[i:j], i, j))
            i = j
            continue
        if c.isalpha() or c == "_":
            j = i
            while j < n and (s[j].isalnum() or s[j] in "_."):
                j += 1
            toks.append(("ID", s[i:j], i, j))
            i = j
            continue
        raise ValueError(f"unrecognized character {c!r} at {i} in {s!r}")
    return toks


# op -> (level, has_space) ; higher level binds tighter.
BINOPS = {
    "==": (1, True), "<=": (1, True), "<": (1, True), ">=": (1, True), ">": (1, True),
    "|": (2, True),
    "^": (3, True),
    "<<": (4, True), ">>": (4, True),
    "+": (5, True), "-": (5, True),
    "*": (6, False), "/": (6, True), "%": (6, True),
}
UNARY_LEVEL = 7


class Parser:
    def __init__(self, src):
        self.src = src
        self.toks = tokenize(src)
        self.pos = 0

    def peek(self):
        return self.toks[self.pos] if self.pos < len(self.toks) else None

    def advance(self):
        t = self.toks[self.pos]
        self.pos += 1
        return t

    def parse(self):
        node = self.parse_expr(0)
        if self.pos != len(self.toks):
            raise ValueError(f"trailing tokens at {self.pos}: {self.toks[self.pos:]}")
        return node

    def parse_expr(self, min_level):
        left = self.parse_unary()
        while True:
            tok = self.peek()
            if tok is None or tok[0] != "OP" or tok[1] not in BINOPS:
                break
            op = tok[1]
            level, _ = BINOPS[op]
            if level < min_level:
                break
            self.advance()
            right = self.parse_expr(level + 1)
            left = ("bin", op, left, right)
        return left

    def parse_unary(self):
        tok = self.peek()
        if tok is not None and tok[0] == "OP" and tok[1] in ("-", "~", "+"):
            self.advance()
            operand = self.parse_expr(UNARY_LEVEL)
            return ("un", tok[1], operand)
        return self.parse_atom()

    def parse_atom(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of input")
        kind, text, start, end = tok
        if kind == "NUM":
            self.advance()
            return ("num", text)
        if kind == "OP" and text == "(":
            self.advance()
            inner = self.parse_expr(0)
            close = self.peek()
            if close is None or close[1] != ")":
                raise ValueError("expected )")
            self.advance()
            return ("paren", inner)
        if kind == "ID":
            self.advance()
            nxt = self.peek()
            # call iff '(' is immediately adjacent (no whitespace) to the name
            if nxt is not None and nxt[1] == "(" and nxt[2] == end:
                self.advance()  # consume '('
                args = []
                if self.peek() is not None and self.peek()[1] != ")":
                    args.append(self.parse_expr(0))
                    while self.peek() is not None and self.peek()[1] == ",":
                        self.advance()
                        args.append(self.parse_expr(0))
                close = self.peek()
                if close is None or close[1] != ")":
                    raise ValueError("expected ) closing call " + text)
                self.advance()
                return ("call", text, args)
            if text.startswith("v") and text[1:].isdigit():
                return ("var", text)
            return ("id", text)
        raise ValueError(f"unexpected token {tok}")


def parse_text(s):
    return Parser(s).parse()


def print_node(node):
    kind = node[0]
    if kind == "num":
        return node[1]
    if kind == "var" or kind == "id":
        return node[1]
    if kind == "call":
        _, name, args = node
        return f"{name}(" + ", ".join(print_node(a) for a in args) + ")"
    if kind == "paren":
        return "(" + print_node(node[1]) + ")"
    if kind == "un":
        _, op, operand = node
        return op + print_node(operand)
    if kind == "bin":
        _, op, l, r = node
        _, has_space = BINOPS[op]
        sep = f" {op} " if has_space else op
        return print_node(l) + sep + print_node(r)
    raise ValueError(f"unknown node kind {kind}")


def strip_paren(node):
    """Unwrap explicit-grouping paren nodes for structural comparison
    and matching -- they carry no semantic content, only print shape."""
    while node[0] == "paren":
        node = node[1]
    if node[0] == "call":
        return ("call", node[1], [strip_paren(a) for a in node[2]])
    if node[0] == "un":
        return ("un", node[1], strip_paren(node[2]))
    if node[0] == "bin":
        return ("bin", node[1], strip_paren(node[2]), strip_paren(node[3]))
    return node


def structurally_equal(a, b):
    a, b = strip_paren(a), strip_paren(b)
    if a[0] != b[0]:
        return False
    if a[0] in ("num", "var", "id"):
        return a[1] == b[1]
    if a[0] == "un":
        return a[1] == b[1] and structurally_equal(a[2], b[2])
    if a[0] == "bin":
        return a[1] == b[1] and structurally_equal(a[2], b[2]) and structurally_equal(a[3], b[3])
    if a[0] == "call":
        if a[1] != b[1] or len(a[2]) != len(b[2]):
            return False
        return all(structurally_equal(x, y) for x, y in zip(a[2], b[2]))
    return False


def is_var_or_literal(node):
    node = strip_paren(node)
    return node[0] in ("num", "var")


def to_pattern(node):
    """Replace each distinct v<N> with a HOLE node ('hole', name);
    the hole's identity is the variable name itself, so two
    occurrences of v0 become the same hole."""
    node = strip_paren(node)
    if node[0] == "var":
        return ("hole", node[1])
    if node[0] == "num" or node[0] == "id":
        return node
    if node[0] == "un":
        return ("un", node[1], to_pattern(node[2]))
    if node[0] == "bin":
        return ("bin", node[1], to_pattern(node[2]), to_pattern(node[3]))
    if node[0] == "call":
        return ("call", node[1], [to_pattern(a) for a in node[2]])
    raise ValueError(node)


def match(pattern, tree, bindings):
    """Match `pattern` (a pattern tree, holes = ('hole', name)) against
    `tree` (a plain parsed tree, already strip_paren'd), filling
    `bindings` (hole name -> tree). Returns True/False; bindings is
    mutated on success paths only (caller should copy before trying)."""
    tree = strip_paren(tree)
    if pattern[0] == "hole":
        name = pattern[1]
        if name in bindings:
            return structurally_equal(bindings[name], tree)
        bindings[name] = tree
        return True
    if pattern[0] != tree[0]:
        return False
    if pattern[0] in ("num", "id"):
        return pattern[1] == tree[1]
    if pattern[0] == "un":
        return pattern[1] == tree[1] and match(pattern[2], tree[2], bindings)
    if pattern[0] == "bin":
        return (pattern[1] == tree[1]
                and match(pattern[2], tree[2], bindings)
                and match(pattern[3], tree[3], bindings))
    if pattern[0] == "call":
        if pattern[1] != tree[1] or len(pattern[2]) != len(tree[2]):
            return False
        for p, t in zip(pattern[2], tree[2]):
            if not match(p, t, bindings):
                return False
        return True
    return False


def try_match_root(pattern, tree):
    bindings = {}
    if match(pattern, tree, bindings):
        return bindings
    return None


def main():
    t_start = time.time()
    with open(POOL_PATH) as f:
        pool = json.load(f)
    with open(CROSS1_PATH) as f:
        cross1 = json.load(f)

    entries = pool["entries"]
    entry_by_id = {e["entry_id"]: e for e in entries}

    # ---- 1. round-trip test over every distinct layer-5 text ----
    distinct_texts = set()
    for e in entries:
        for t in e.get("layer5_normalized_texts", []):
            distinct_texts.add(t)
    distinct_texts = sorted(distinct_texts)

    failures = []
    parsed_cache = {}
    for t in distinct_texts:
        try:
            node = parse_text(t)
            reprinted = print_node(node)
            if reprinted != t:
                failures.append((t, reprinted, None))
            else:
                parsed_cache[t] = node
        except Exception as exc:  # noqa: BLE001
            failures.append((t, None, repr(exc)))

    print(f"round-trip: {len(distinct_texts)} distinct layer-5 texts, "
          f"{len(failures)} failures")
    for t, reprinted, err in failures[:3]:
        print("FAILURE text:", t)
        print("  reprinted:", reprinted)
        print("  error:", err)
    if failures:
        print(f"[stop-rule] {len(failures)} texts excluded from length-two "
              f"matching, not patched per text (brief section 4/5).")

    # entry_id -> {lang: text} using only round-trip-clean texts
    entry_text_by_lang = {}
    for e in entries:
        eid = e["entry_id"]
        by_lang = {}
        for m in e["members"]:
            txt = m["layer5_normalized_text"]
            if txt in parsed_cache:
                by_lang.setdefault(m["lang"], txt)
        entry_text_by_lang[eid] = by_lang

    matrix_langs = cross1["matrix_languages"]

    # patterns per language: dedupe by text, dropping texts that failed
    # to round-trip.
    lang_patterns = {}  # lang -> list of (text, pattern_ast, entry_id_example)
    for lang in matrix_langs:
        seen = {}
        for e in entries:
            for m in e["members"]:
                if m["lang"] != lang:
                    continue
                txt = m["layer5_normalized_text"]
                if txt not in parsed_cache or txt in seen:
                    continue
                seen[txt] = e["entry_id"]
        pats = []
        for txt, eid in seen.items():
            pats.append((txt, to_pattern(parsed_cache[txt]), eid))
        lang_patterns[lang] = pats
        print(f"lang {lang}: {len(pats)} distinct round-trip-clean patterns")

    pairs = {}
    table_rows = []
    quoted_constructions = []
    quoted_misses = []

    lane_deadline_hit = False
    for x in matrix_langs:
        row = {"x": x, "cells": {}}
        x_pats = lang_patterns[x]
        for y in matrix_langs:
            if x == y:
                continue
            key = f"{x}|{y}"
            cell1 = cross1["pairs"][key]
            not_built_ids = cell1["not_built_entry_ids"]

            sampled = False
            candidate_ids = not_built_ids
            if time.time() - t_start > TIME_BUDGET_S and len(not_built_ids) > SAMPLE_SIZE:
                import random
                rng = random.Random(1234567)
                candidate_ids = sorted(rng.sample(not_built_ids, SAMPLE_SIZE))
                sampled = True
                lane_deadline_hit = True

            built_len2 = []
            constructions = {}
            misses = []
            for eid in candidate_ids:
                ytext = entry_text_by_lang[eid].get(y)
                if ytext is None:
                    continue  # y's own text failed round-trip; excluded
                ytree = strip_paren(parsed_cache[ytext])
                found = None
                for xtext, xpat, xeid in x_pats:
                    b = try_match_root(xpat, ytree)
                    if b is None:
                        continue
                    ok = True
                    inner_used = {}
                    for hole_name, subtree in b.items():
                        if is_var_or_literal(subtree):
                            inner_used[hole_name] = {"kind": "var_or_literal",
                                                      "text": print_node(subtree)}
                            continue
                        inner_ok = False
                        for xtext2, xpat2, xeid2 in x_pats:
                            b2 = try_match_root(xpat2, subtree)
                            if b2 is None:
                                continue
                            if all(is_var_or_literal(v) for v in b2.values()):
                                inner_ok = True
                                inner_used[hole_name] = {
                                    "kind": "matched_x_pattern",
                                    "x_pattern_text": xtext2,
                                    "x_example_entry": xeid2,
                                    "text": print_node(subtree),
                                    "bindings": {h: print_node(v) for h, v in b2.items()},
                                }
                                break
                        if not inner_ok:
                            ok = False
                            break
                    if ok:
                        found = {
                            "root_x_pattern_text": xtext,
                            "root_x_example_entry": xeid,
                            "bindings": inner_used,
                        }
                        break
                if found is not None:
                    built_len2.append(eid)
                    constructions[eid] = found
                else:
                    misses.append(eid)

            total_not_built = len(not_built_ids)
            considered = len(candidate_ids)
            pct = (100.0 * len(built_len2) / considered) if considered else 0.0
            pairs[key] = {
                "x": x, "y": y,
                "built_len2_entry_ids": sorted(built_len2),
                "still_not_built_entry_ids": sorted(misses),
                "built_len2_count": len(built_len2),
                "not_built_len1_count": total_not_built,
                "sampled": sampled,
                "sample_size_considered": considered,
                "percent_built_len2_of_considered": round(pct, 2),
                "constructions": constructions,
            }
            row["cells"][y] = (f"{len(built_len2)}/{considered}"
                                f"{'*' if sampled else ''} ({pct:.1f}%)")

            for eid, c in list(constructions.items())[:3]:
                quoted_constructions.append({
                    "pair": key, "entry_id": eid,
                    "y_text": entry_text_by_lang[eid].get(y),
                    "construction": c,
                })
            for eid in misses[:3]:
                quoted_misses.append({
                    "pair": key, "entry_id": eid,
                    "y_text": entry_text_by_lang[eid].get(y),
                })
        table_rows.append(row)

    out = {
        "task": "o1 deliverable B -- length-two construction map",
        "parser_round_trip": {
            "distinct_layer5_texts": len(distinct_texts),
            "failures": len(failures),
            "failure_examples": [
                {"text": t, "reprinted": r, "error": e} for t, r, e in failures[:3]
            ],
        },
        "lane_time_budget_s": TIME_BUDGET_S,
        "lane_deadline_hit_any_pair": lane_deadline_hit,
        "sample_size_when_sampled": SAMPLE_SIZE,
        "matrix_languages": matrix_langs,
        "pairs": pairs,
        "table_rows": table_rows,
        "quoted_constructions_sample": quoted_constructions[:12],
        "quoted_misses_sample": quoted_misses[:12],
    }
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    total = len(matrix_langs) * (len(matrix_langs) - 1)
    print()
    print("| x \\ y | " + " | ".join(matrix_langs) + " |")
    print("|---" * (len(matrix_langs) + 1) + "|")
    for row in table_rows:
        cells = [row["cells"].get(y, "--") for y in matrix_langs]
        print(f"| {row['x']} | " + " | ".join(cells) + " |")
    i = 0
    for key in pairs:
        i += 1
        print(f"[{i}/{total}] pair {key} done")
    print("elapsed_s", round(time.time() - t_start, 1))
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    main()
