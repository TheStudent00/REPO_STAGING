#!/usr/bin/env python3
"""validate.py — does the clustering RECREATE the known cross-language
overlap? Ground truth is the explicit table below: rows of kinds that are
known correspondences across the five languages. For each row we report
co-clustered fully / partially (naming strays and where they went) /
scattered, then the converse (clusters mixing rows = over-merging), and a
simple purity score: over all ground-truth members, the fraction sitting in
a cluster whose ground-truth majority is their own row.

A row lists one kind per language where a clear counterpart exists; a
language is omitted from a row when the grammar has no comparable kind.
"""
import json
import os
import collections

HERE = os.path.dirname(os.path.abspath(__file__))

GROUND_TRUTH = {
    "binary_expression": ["rust:binary_expression", "python:binary_operator",
                          "dart:additive_expression", "c:binary_expression",
                          "cpp:binary_expression"],
    "if_conditional": ["rust:if_expression", "python:if_statement",
                       "dart:if_statement", "c:if_statement",
                       "cpp:if_statement"],
    "function_definition": ["rust:function_item", "python:function_definition",
                            "dart:function_signature", "c:function_definition",
                            "cpp:function_definition"],
    "call": ["rust:call_expression", "python:call",
             "c:call_expression", "cpp:call_expression"],  # dart: no single call kind
    "parameter_list": ["rust:parameters", "python:parameters",
                       "dart:formal_parameter_list", "c:parameter_list",
                       "cpp:parameter_list"],
    "identifier": ["rust:identifier", "python:identifier", "dart:identifier",
                   "c:identifier", "cpp:identifier"],
    "string_literal": ["rust:string_literal", "python:string",
                       "dart:string_literal", "c:string_literal",
                       "cpp:string_literal"],
    "number_literal": ["rust:integer_literal", "python:integer",
                       "dart:decimal_integer_literal", "c:number_literal",
                       "cpp:number_literal"],
    "assignment": ["rust:assignment_expression", "python:assignment",
                   "dart:assignment_expression", "c:assignment_expression",
                   "cpp:assignment_expression"],
    "for_loop": ["rust:for_expression", "python:for_statement",
                 "dart:for_statement", "c:for_statement", "cpp:for_statement"],
    "while_loop": ["rust:while_expression", "python:while_statement",
                   "dart:while_statement", "c:while_statement",
                   "cpp:while_statement"],
    "return": ["rust:return_expression", "python:return_statement",
               "dart:return_statement", "c:return_statement",
               "cpp:return_statement"],
    "field_access": ["rust:field_expression", "python:attribute",
                     "c:field_expression", "cpp:field_expression"],  # dart: selector-based, no counterpart
    "block": ["rust:block", "python:block", "dart:block",
              "c:compound_statement", "cpp:compound_statement"],
    "argument_list": ["rust:arguments", "python:argument_list",
                      "dart:arguments", "c:argument_list",
                      "cpp:argument_list"],
}


def main():
    data = json.load(open(os.path.join(HERE, "clusters.json")))
    member_to_cluster = {}
    for cid, members in data["clusters"].items():
        for m in members:
            member_to_cluster[m] = cid

    lines = []
    def emit(s=""):
        print(s)
        lines.append(s)

    emit("validation of clusters.json against %d ground-truth rows" %
         len(GROUND_TRUTH))
    emit()

    correct = 0
    total = 0
    row_of = {}
    verdict_rows = []
    for row, members in GROUND_TRUTH.items():
        for m in members:
            row_of[m] = row
        cids = collections.Counter()
        missing = [m for m in members if m not in member_to_cluster]
        for m in members:
            if m in member_to_cluster:
                cids[member_to_cluster[m]] += 1
        if missing:
            emit("row %s: MISSING members (not clustered): %s" % (row, missing))
        top_cid, top_n = cids.most_common(1)[0]
        n = sum(cids.values())
        if len(cids) == 1:
            verdict = "fully"
            detail = "all %d in %s" % (n, top_cid)
        elif top_n >= 2:
            verdict = "partially"
            strays = ["%s->%s" % (m, member_to_cluster[m]) for m in members
                      if m in member_to_cluster and member_to_cluster[m] != top_cid]
            detail = "%d/%d in %s; strayed: %s" % (top_n, n, top_cid,
                                                   ", ".join(strays))
        else:
            verdict = "scattered"
            detail = "; ".join("%s->%s" % (m, member_to_cluster[m])
                               for m in members if m in member_to_cluster)
        verdict_rows.append((row, verdict, detail))
        emit("row %-20s %-10s %s" % (row, verdict, detail))

    emit()
    # Purity: majority-row correctness over ground-truth members.
    by_cluster = collections.defaultdict(list)
    for m, row in row_of.items():
        if m in member_to_cluster:
            by_cluster[member_to_cluster[m]].append(row)
    for cid, rows in sorted(by_cluster.items()):
        cnt = collections.Counter(rows)
        maj = cnt.most_common(1)[0][1]
        correct += maj
        total += len(rows)
        if len(cnt) > 1:
            emit("over-merge: cluster %s mixes rows %s" %
                 (cid, dict(cnt)))
    purity = correct / total
    emit()
    emit("purity (majority-row fraction over %d ground-truth members): %.3f"
         % (total, purity))
    fully = sum(1 for _, v, _ in verdict_rows if v == "fully")
    partially = sum(1 for _, v, _ in verdict_rows if v == "partially")
    emit("rows fully co-clustered: %d/%d; partially: %d; scattered: %d" %
         (fully, len(verdict_rows), partially,
          len(verdict_rows) - fully - partially))

    with open(os.path.join(HERE, "validation.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", os.path.join(HERE, "validation.txt"))


if __name__ == "__main__":
    main()
