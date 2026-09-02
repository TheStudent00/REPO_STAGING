#!/usr/bin/env python3
"""compare_v2.py — measure the effect of the decision-6 counts fix (v2)
on the 5-language spectrum: identical-feature pair splits, hold-out AUC
summary, and survival of the log_010 SS6 stable clusters.
Vocabulary: super-node / sub-node / co-node / sub-tree only."""
import json
import os
import numpy as np
import spectrum

HERE = os.path.dirname(os.path.abspath(__file__))


def identical_pairs(fname):
    feats = json.load(open(os.path.join(HERE, fname)))
    items = []
    for lang in sorted(feats):
        for kind in sorted(feats[lang]):
            f = feats[lang][kind]["features"]
            key = json.dumps({k: repr(v) for k, v in sorted(f.items())},
                             sort_keys=True)
            items.append((lang, lang + ":" + kind, key))
    groups = {}
    for lang, label, key in items:
        groups.setdefault(key, []).append((lang, label))
    pairs = set()
    for mem in groups.values():
        for i in range(len(mem)):
            for j in range(i + 1, len(mem)):
                if mem[i][0] != mem[j][0]:
                    pairs.add(tuple(sorted((mem[i][1], mem[j][1]))))
    return pairs


def main():
    p1 = identical_pairs("features.json")
    p2 = identical_pairs("features_v2.json")
    ccp1 = {p for p in p1 if {p[0].split(":")[0], p[1].split(":")[0]} ==
            {"c", "cpp"}}
    non1 = p1 - ccp1
    surv = non1 & p2
    print("v1 identical cross-language pairs: %d (c-cpp twins %d, other %d)"
          % (len(p1), len(ccp1), len(non1)))
    print("v2 identical cross-language pairs: %d" % len(p2))
    print("of the %d non-c/cpp v1 identical pairs, %d split under v2, "
          "%d remain identical" % (len(non1), len(non1 - p2), len(surv)))
    print("of the %d c-cpp twin pairs, %d remain identical" %
          (len(ccp1), len(ccp1 & p2)))

    # hold-out AUC summary v1 vs v2
    for tag in ("", "_v2"):
        d = json.load(open(os.path.join(
            HERE, "holdout_validation%s.json" % (tag or ""))))
        aucs = [r["auc"] for r in d["per_supertype"]]
        wi = [r["mean_within"] for r in d["per_supertype"]]
        ac = [r["mean_across"] for r in d["per_supertype"]]
        print("hold-out %s: mean AUC %.3f median %.3f, %d/%d >= 0.6, "
              "mean within %.3f vs across %.3f; hand key AUC %.3f" %
              (tag or "v1", np.mean(aucs), np.median(aucs),
               sum(a >= 0.6 for a in aucs), len(aucs),
               np.mean(wi), np.mean(ac),
               d["hand_key_secondary"]["auc_vs_background"]))

    # log_010 SS6 stable clusters: do they survive in the v2 tree?
    stable = {
        "s066": ["c:else_clause", "cpp:else_clause"],
        "s024": ["c:preproc_call", "c:preproc_include", "cpp:preproc_call",
                 "cpp:preproc_include", "python:format_expression",
                 "python:interpolation", "rust:qualified_type"],
        "s069": ["c:linkage_specification", "cpp:linkage_specification"],
        "s043": ["c:preproc_elif", "c:preproc_if", "cpp:preproc_elif",
                 "cpp:preproc_if"],
        "s018": ["c:gnu_asm_clobber_list", "c:gnu_asm_goto_list",
                 "c:gnu_asm_input_operand_list",
                 "c:gnu_asm_output_operand_list",
                 "c:subscript_range_designator",
                 "cpp:gnu_asm_clobber_list", "cpp:gnu_asm_goto_list",
                 "cpp:gnu_asm_input_operand_list",
                 "cpp:gnu_asm_output_operand_list",
                 "cpp:subscript_range_designator"],
        "s064": ["c:case_statement", "cpp:case_statement"],
        "s070": ["c:preproc_defined", "cpp:preproc_defined"],
        "s026": ["c:comment", "cpp:comment", "dart:comment",
                 "dart:documentation_comment", "python:comment",
                 "python:line_continuation"],
        "s051": ["c:parameter_list", "c:preproc_params",
                 "cpp:preproc_params"],
        "s065": ["c:comma_expression", "cpp:comma_expression"],
        "s084_lambda": ["python:lambda", "rust:closure_expression"],
        "s049_cond": ["c:conditional_expression", "cpp:conditional_expression",
                      "rust:if_expression"],
        "s013_param": None,  # size-11 family checked by pair sim below
        "s012_loop": ["c:do_statement", "c:for_statement",
                      "c:switch_statement", "c:while_statement",
                      "cpp:do_statement", "cpp:for_statement",
                      "cpp:switch_statement", "cpp:while_statement",
                      "dart:do_statement", "dart:switch_statement",
                      "dart:while_statement"],
        "s009_bodies": ["c:declaration_list", "c:enumerator_list",
                        "c:field_declaration_list", "cpp:declaration_list",
                        "cpp:enumerator_list", "cpp:field_declaration_list",
                        "dart:class_body", "dart:enum_body",
                        "dart:extension_body", "dart:switch_block",
                        "rust:declaration_list", "rust:enum_variant_list",
                        "rust:field_declaration_list",
                        "rust:field_initializer_list", "rust:match_block",
                        "rust:ordered_field_declaration_list"],
    }
    bands = spectrum.stability_bands(os.path.join(HERE,
                                     "similarity_matrix_v2.npz"))
    labels, Z, S = spectrum.load_spectrum(
        os.path.join(HERE, "similarity_matrix_v2.npz"))
    idx = {l: i for i, l in enumerate(labels)}
    print("\nlog_010 SS6 stable clusters under v2:")
    for name, mem in stable.items():
        if mem is None:
            continue
        fs = frozenset(mem)
        if fs in bands:
            b, d = bands[fs]
            print("  %-12s SURVIVES exact, band %.2f-%.2f (width %.2f)" %
                  (name, b, d, d - b))
        else:
            ids = [idx[m] for m in mem if m in idx]
            sub = S[np.ix_(ids, ids)]
            mn = sub[np.triu_indices(len(ids), 1)].min() if len(ids) > 1 else 1
            # find smallest merge-tree node containing all members
            best = None
            for ms, (b, d) in bands.items():
                if fs <= ms and (best is None or len(ms) < len(best[0])):
                    best = (ms, b, d)
            print("  %-12s not exact; min internal sim %.2f; smallest "
                  "containing sub-tree size %d (band %.2f-%.2f)" %
                  (name, mn, len(best[0]), best[1], best[2]))

    # saturation count under v2
    raw = spectrum.load_spectrum.raw
    iu = np.triu_indices(len(labels), 1)
    lang_of = np.array([l.split(":")[0] for l in labels])
    cross = lang_of[iu[0]] != lang_of[iu[1]]
    sat = (raw[iu] < 1e-9) & cross
    print("\nv2 saturated (raw distance 0) cross-language pairs: %d"
          % sat.sum())


if __name__ == "__main__":
    main()
