"""System -- the three passes over the model and the languages, in one
method, producing the dictionary; the loop the owner wrote on 2026-09-13, as
code. Plan leaf: lean_proof_path.system, with methods run, pass_a_find,
pass_b_build, pass_c_units_across_languages.

Nothing in it names an opcode; the population is every definition the
model gives and every unit the compilers gave. Every pass rests on
ArchUnit.meaning and LeanExpr.equals, which rest on the built model.
"""

import json
import os
import re
import time

from .arch_unit import ArchUnit
from .lean_expr import LeanExpr
from .emulation import Emulation

AWAITS_BUILT_MODEL = "AWAITS_BUILT_MODEL"


class System:
    """attributes: model, langs, dictionary."""

    def __init__(self, model, langs, dictionary):
        self.model = model
        self.langs = langs
        self.dictionary = dictionary

    @staticmethod
    def run(model, langs, dictionary):
        """run(model, langs) -> Dictionary.
        1. defs = model.definitions()
        2. for every language, for every unit in its corpus:
           unit.lean = unit.meaning(defs)
        3. pass_a_find; pass_b_build; pass_c_units_across_languages
        4. return the dictionary, with every refusal as a row
        lp1 runs pass A alone (brief section 2); `run` is the composition."""
        return {"refusal": "lp1 runs pass_a_find alone; run composes the three passes"}

    @staticmethod
    def candidates(unit_form, def_forms):
        """the candidate definitions for a unit: machine-form evidence
        only -- every definition instance whose operand form carries no
        immediate (the unit's interface is registers in, a register out),
        in key order. An immediate-form instance is tried only at the
        immediates the model's own decoder read from the unit's words
        (added by the caller); nothing is chosen by a name."""
        return [k for k in def_forms if not def_forms[k].get("unknowns")]

    @staticmethod
    def pass_a_find(units, def_forms, project, workdir, hyps, budget_s, tag, stop_at=None):
        """pass_a_find(defs, langs, dictionary): for every unit, for every
        candidate definition: equals(definition, unit.lean) proves -> an
        Emulation marked found; every Differ and Undecided is a row with
        its stage. Whoever gets there first, by proof over what the
        compiler already emitted, with no render. `operator_for` (the
        swap table) is filled from the entries found: the unit that
        proves a definition is the language's operator for that
        definition's primitives at its width.

        The order per pair, the plan's: the two printed forms compared
        as text first (identical text -> the theorem is `rfl`, checked
        in Lean all the same); else the point test on the certified
        forms (a differing point is `Differ` with the input); else the
        staged `equals`."""
        rows = []
        found = []
        t_start = time.time()
        for ui, u in enumerate(units):
            if stop_at and time.time() - t_start > stop_at:
                rows.append({"unit": u["label"], "outcome": "not reached", "stage": "the lane's time bound %ds" % stop_at})
                continue
            if "expr" not in u["meaning"]:
                rows.append({"unit": u["label"], "outcome": "Refused", "stage": "meaning: " + u["meaning"].get("refusal", "")})
                continue
            uform = u["meaning"]["answer"]
            hit = None
            for key in System.candidates(uform, def_forms):
                d = def_forms[key]
                if "expr" not in d:
                    continue
                name = "%s_%s_vs_%s" % (tag, re.sub(r'[^A-Za-z0-9]', '_', u["label"])[:60], re.sub(r'[^A-Za-z0-9]', '_', "_".join(key)))
                if d["answer"] == uform:
                    verdict = LeanExpr.equals(u["meaning"]["expr"], d["expr"], budget_s, project, workdir, name)
                    verdict["by"] = "identical text, checked"
                else:
                    if u.get("points_fn") and d.get("points_fn"):
                        pt = LeanExpr.decide_fixed_width(u["points_fn"], d["points_fn"], project, workdir, name, POINTS)
                        if pt["outcome"] == "Differ":
                            rows.append({"unit": u["label"], "key": key, "outcome": "Differ", "stage": "point test", "input": pt["input"], "seconds": pt["seconds"]})
                            continue
                    verdict = LeanExpr.equals(u["meaning"]["expr"], d["expr"], budget_s, project, workdir, name)
                    verdict["by"] = "staged"
                row = {"unit": u["label"], "key": key, "outcome": verdict["outcome"], "stage": verdict.get("stage"), "seconds": verdict.get("seconds"), "file": verdict.get("file")}
                if verdict["outcome"] == "Proof":
                    hit = row
                    found.append(Emulation(key, u["language"], u["label"], verdict["file"], "found", tag))
                rows.append(row)
                if hit:
                    break
            if hit is None:
                rows.append({"unit": u["label"], "outcome": "no candidate proved", "stage": "pass A"})
        return rows, found

    @staticmethod
    def pass_b_build(defs, langs, dictionary):
        """pass_b_build: for every (definition, language) pass A left
        empty: render, compile, meaning, equals. Not run in lp1."""
        return {"refusal": "NOT_RUN_IN_LP1"}

    @staticmethod
    def pass_c_units_across_languages(langs, dictionary):
        """pass_c_units_across_languages: units against units across
        languages (the Hub's ground). OUT OF SCOPE for task lp1 (brief
        section 1): a stub that says so."""
        return {"refusal": "OUT_OF_SCOPE_FOR_LP1"}


# the points of the counterexample search: edge values of a 64-bit
# register and two ordinary ones, every argument register the same list
POINTS_1 = ["0#64", "1#64", "0xffffffffffffffff#64", "0x8000000000000000#64", "0x7fffffffffffffff#64", "5#64", "0xfffffffffffffffd#64", "0x123456789abcdef0#64"]
POINTS = []
for _a in POINTS_1:
    for _b in POINTS_1[::-1]:
        POINTS.append([_a, _b] + ["0#64"] * 6)
POINTS = POINTS[:24]
