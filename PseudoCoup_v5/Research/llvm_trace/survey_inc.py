#!/usr/bin/env python3
"""Grammar/shape survey of generated .inc files, same methodology as the
Cranelift assembler.rs survey (see DevComms/project_state.md 2026-07-25
GROUND TRUTH entry): classify every code line by syntactic shape, count
comment/blank vs code, report unclassified count, and separately measure
the fraction of lines that are pure dense-table data (the MatcherTable
byte array) vs readable function/control-flow code.

Usage: python3 survey_inc.py <file.inc>
"""
import re
import sys
from collections import Counter

SHAPES = [
    ("blank",             re.compile(r'^\s*$')),
    ("comment_line",      re.compile(r'^\s*//')),
    ("comment_block",     re.compile(r'^\s*/\*.*\*/\s*$')),
    ("preprocessor",      re.compile(r'^\s*#')),
    ("matcher_opcode_row",re.compile(r'\bOPC_[A-Za-z0-9_]+')),  # MatcherTable interpreter opcode mnemonic (data-driven bytecode)
    ("numeric_data_row",  re.compile(r'^[\d\-,\s\|/\*A-Za-z:_#\.\'\(\)]+,\s*(//.*)?$')),  # comma-terminated literal/enum-ref list (table payload)
    ("end_of_scope_row",  re.compile(r'/\*\s*End of Scope\s*\*/')),
    ("struct_init_row",   re.compile(r'^\s*\{.*\},?\s*(//.*)?$')),  # aggregate-initializer table row, e.g. MCInstrDesc entries
    ("enum_member_row",   re.compile(r'^\s*[A-Za-z_][\w:]*(\s*=\s*[^,]+)?,\s*(//.*)?$')),  # enum{...} member list
    ("string_table_row",  re.compile(r'^\s*"')),  # packed string-literal name table entry (address comment stripped)
    ("namespace_line",    re.compile(r'^\s*(namespace|struct|class)\b')),
    ("close_brace_ns",    re.compile(r'^\s*\}\s*//')),
    ("brace_only",        re.compile(r'^\s*[{}]\s*;?\s*$')),
    ("func_decl_def",     re.compile(r'^\s*(void|bool|unsigned|int|SDNode\s*\*|uint\d+_t|static)\b.*\(.*\)\s*(const)?\s*\{?\s*$')),
    ("return_stmt",       re.compile(r'^\s*return\b')),
    ("if_stmt",           re.compile(r'^\s*(if|else if|else)\s*[\(\{]')),
    ("switch_case",       re.compile(r'^\s*(switch|case|default)\b')),
    ("assignment",        re.compile(r'^\s*[A-Za-z_][\w:\.\->\[\]]*\s*=\s*[^=]')),
    ("assert_stmt",       re.compile(r'^\s*assert\(')),
    ("static_decl",       re.compile(r'^\s*static\s+const')),
]

ADDR_COMMENT = re.compile(r'^\s*/\*\s*\d+\s*\*/\s*')

def classify(line):
    # MatcherTable entries are annotated with a leading byte-offset
    # comment "/*   N*/" — strip it before classifying, otherwise every
    # table row is misclassified as a comment.
    stripped = ADDR_COMMENT.sub('', line)
    if stripped != line and stripped.strip() == '':
        return "table_addr_comment_only"
    for name, pat in SHAPES:
        if pat.search(stripped):
            return name
    return "UNCLASSIFIED"


def main(path):
    with open(path, 'r', errors='replace') as f:
        lines = f.readlines()

    total = len(lines)
    counts = Counter()
    unclassified_samples = []
    matcher_table_lines = 0
    in_matcher_table = False

    for i, raw in enumerate(lines):
        line = raw.rstrip('\n')
        if 'static const unsigned char MatcherTable[]' in line:
            in_matcher_table = True
        shape = classify(line)
        counts[shape] += 1
        if shape == "UNCLASSIFIED" and len(unclassified_samples) < 40:
            unclassified_samples.append((i + 1, line))
        if in_matcher_table:
            matcher_table_lines += 1
        # crude close: a line that is just "};" ends the array
        if in_matcher_table and re.match(r'^\s*\};\s*$', line):
            in_matcher_table = False

    code_lines = total - counts["blank"] - counts["comment_line"] - counts["comment_block"]

    print(f"file: {path}")
    print(f"total lines: {total}")
    print(f"blank: {counts['blank']}  comment_line: {counts['comment_line']}  comment_block: {counts['comment_block']}")
    print(f"code lines (total - blank - comments): {code_lines}")
    print(f"MatcherTable span (inclusive of comments/blank inside it): {matcher_table_lines}")
    print()
    print("shape counts:")
    for name, _ in SHAPES:
        print(f"  {name:20s} {counts[name]}")
    print(f"  {'UNCLASSIFIED':20s} {counts['UNCLASSIFIED']}")
    print()
    print(f"UNCLASSIFIED fraction of total: {counts['UNCLASSIFIED']/total:.4%}")
    print()
    if unclassified_samples:
        print("first UNCLASSIFIED samples:")
        for ln, txt in unclassified_samples:
            print(f"  {ln}: {txt[:140]}")


if __name__ == "__main__":
    main(sys.argv[1])
