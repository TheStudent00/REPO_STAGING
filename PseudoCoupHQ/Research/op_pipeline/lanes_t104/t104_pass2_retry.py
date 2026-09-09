#!/usr/bin/env python3
"""t104_pass2_retry.py -- LAW's "time or memory limits are FLAGS" rule,
applied to lane 10's own pass-2 tail.

WHAT LANE 10 MEASURED.  Its pass 2 ran at a 3,072 MB / 900 s ceiling,
three workers at once (so 3 x the ceiling fits the instance's declared
8g).  204 units were flagged in pass 1; 184 of them still failed in
pass 2, EVERY ONE for `MEMORY_REASON`, wall time 0.93-1.77 s (not a
timeout) and sub-process peak resident 3,009,820-3,087,212 kB -- right
at the 3,072 MB (3,145,728 kB) ceiling.  That is a ceiling that is too
small for these units under the changed normalizer, not a
non-terminating computation: LAW says re-run with more room and report
whether the answer changed, never leave the ceiling as the answer.

WHAT THIS PROGRAM DOES.  It imports `t104_walk.py` UNCHANGED -- no
edit to that file -- and calls its own `run_pass2` again, at a HIGHER
ceiling, over ONLY the 184 units still short, with the worker count
turned down to 1 (a module-level monkeypatch on the imported object,
not a file edit) so the whole retry's memory is bounded by the one
ceiling and not 3x it, and stays inside the instance's declared 8g
with the fork-per-unit isolation `one_unit_forked` already provides.
`run_pass2`, `pass2_worker`, `one_unit_forked`, `text_delta` and the
summary/document shape are ALL the original functions, called, not
duplicated -- so a unit that converges this way merges into
`term104_store/` exactly the way lane 10's own pass 2 would have
merged it, and `t104_audit.json` / `t104_walk_evidence.json` /
`t104_walk_state.json` are the SAME three files lane 10 wrote, carried
forward rather than replaced.  The first attempt's 184 pass2_rows stay
in `t104_walk_evidence.json`; this retry's rows are appended beside
them, so the file itself shows both ceilings and both outcomes.

WRITES: term104_store/ (merged), t104_walk_state.json,
        t104_walk_evidence.json, t104_audit.json

usage:
  t104_pass2_retry.py <ceiling_mb> <seconds_per_unit>
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import t104_walk as W                                            # noqa: E402


def main():
    ceiling_mb = int(sys.argv[1])
    seconds = int(sys.argv[2])

    W.PASS2_WORKERS = 1

    state = W.load_json(W.STATE, {"shards_done": [], "pass2_done": []})
    evidence = W.load_json(W.EVIDENCE, None)
    if evidence is None:
        raise SystemExit("no t104_walk_evidence.json -- run lane 10 first")

    short_before = sorted(evidence["still_short_after_pass_2"])
    sys.stdout.write(
        "[1/3] %d units still short after lane 10's pass 2, retrying at "
        "%d MB / %d s, 1 worker\n" % (len(short_before), ceiling_mb,
                                       seconds))
    sys.stdout.flush()

    short_set = set(short_before)
    state["pass2_done"] = [name for name in state["pass2_done"]
                           if name not in short_set]
    evidence["still_short_after_pass_2"] = []

    evidence = W.run_pass2(ceiling_mb, seconds, state, evidence)

    W.save_json(W.STATE, state)
    W.save_json(W.EVIDENCE, evidence)

    short_after = sorted(evidence["still_short_after_pass_2"])
    converged = sorted(set(short_before) - set(short_after))
    sys.stdout.write(
        "[2/3] %d of %d converged at the higher ceiling; %d still short\n"
        % (len(converged), len(short_before), len(short_after)))
    sys.stdout.flush()

    changed, before_only, after_only = W.text_delta()
    summary = {
        "retry_ceiling_mb": ceiling_mb,
        "retry_seconds_per_unit": seconds,
        "retry_population": len(short_before),
        "retry_converged": len(converged),
        "retry_still_short": len(short_after),
        "records_re_normalized": evidence["records_re_normalized"],
        "records_no_term": evidence["records_no_term"],
        "records_with_a_term_not_proved":
            evidence["records_with_a_term_not_proved"],
        "records_whose_layer5_text_changed": len(changed),
        "records_in_term66_store_absent_from_term104_store":
            len(after_only),
        "records_in_term104_store_absent_from_term66_store":
            len(before_only),
        "layer4_sexpr_hash_disagreements":
            len(evidence["layer4_hash_disagreements"]),
        "records_flagged_in_pass_1": len(evidence["flagged"]),
        "records_still_short_after_pass_2": len(short_after),
        "canon40_units_proved": evidence["canon40_units_proved"],
        "canon40_proved_units_with_no_term66_record":
            len(evidence["units_with_no_term66_record"]),
        "operand_order_acceptance_units_checked":
            evidence["perturbation_units_checked"],
        "operand_order_acceptance_units_with_a_node_moved":
            evidence["perturbation_units_with_a_node_moved"],
        "operand_order_acceptance_nodes_reordered":
            evidence["perturbation_nodes_reordered"],
        "operand_order_acceptance_disagreements":
            len(evidence["perturbation_disagreements"]),
    }
    document = {
        "summary": summary,
        "converged_on_retry": converged,
        "still_short_after_pass_2_before_retry": short_before,
        "changed_records": changed,
        "records_in_term66_store_absent_from_term104_store":
            sorted(after_only),
        "records_in_term104_store_absent_from_term66_store":
            sorted(before_only),
        "layer4_sexpr_hash_disagreements":
            evidence["layer4_hash_disagreements"],
        "operand_order_acceptance": {
            "what_it_measures":
                "for each unit a second term was built by permuting "
                "the operands of every commutative node, with the "
                "permutation drawn from random.Random('t104|<unit>'); "
                "both terms were normalized; the property holds when "
                "the two texts are the same string",
            "population":
                "the units pass 1 walked; the units pass 2 answered "
                "were not perturbation-checked and are named in "
                "pass2_units",
            "units_checked": evidence["perturbation_units_checked"],
            "units_with_a_node_moved":
                evidence["perturbation_units_with_a_node_moved"],
            "nodes_reordered":
                evidence["perturbation_nodes_reordered"],
            "disagreements": evidence["perturbation_disagreements"],
        },
        "pass2_units": evidence["pass2_rows"],
        "records_still_short_after_pass_2": short_after,
        "canon40_proved_units_with_no_term66_record":
            sorted(evidence["units_with_no_term66_record"]),
        "declaration_kind_census": evidence["declaration_kind_census"],
        "commutative_table_in_term_py": {
            "plain": sorted(W.T.COMMUTATIVE_OPERATORS),
            "rounded": sorted(W.T.ROUNDED_COMMUTATIVE_OPERATORS),
        },
    }
    W.save_json(W.AUDIT, document)
    sys.stdout.write("[3/3] wrote %s\n" % W.AUDIT)
    sys.stdout.write(json.dumps(summary, indent=1, sort_keys=True))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
