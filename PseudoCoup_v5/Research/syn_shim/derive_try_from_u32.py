#!/usr/bin/env python3
"""The TryFromU32 derive, reimplemented against syn_shim.

The real definition is `macro_rules! TryFromU32` in
rustc_codegen_llvm/src/macros.rs — one of the six files the stock
grammar cannot parse. Its template, read from that file:

    impl TryFrom<u32> for $Type {
        type Error = u32;
        fn try_from(value: u32) -> Result<$Type, u32> {
            $( if value == const { $Type::$Variant as u32 }
                 { return Ok($Type::$Variant) } )*
            Err(value)
        }
    }

Below: the same logic as a Python function over the shim — which is
what a transpiled proc macro would look like at this level. Run via
run.sh, which extracts the real CovmapVersion enum from the vendored
corpus first.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from syn_shim import parse_derive_input, DataEnum  # noqa: E402


def derive_try_from_u32(source: str) -> str:
    inp = parse_derive_input(source)
    assert isinstance(inp.data, DataEnum), "TryFromU32 is for enums"
    t = inp.ident
    arms = "\n".join(
        f"        if value == const {{ {t}::{v.ident} as u32 }} "
        f"{{ return Ok({t}::{v.ident}); }}"
        for v in inp.data.variants)
    return (f"impl ::core::convert::TryFrom<u32> for {t} {{\n"
            f"    type Error = u32;\n"
            f"    fn try_from(value: u32) -> "
            f"::core::result::Result<{t}, u32> {{\n"
            f"{arms}\n"
            f"        Err(value)\n"
            f"    }}\n"
            f"}}")


if __name__ == "__main__":
    enum_path = sys.argv[1] if len(sys.argv) > 1 else "real_enum.rs"
    real = open(enum_path).read()
    print("== INPUT (real, from the corpus):")
    print(real)
    print("== OUTPUT (the expansion, produced by shim + python logic):")
    out = derive_try_from_u32(real)
    print(out)

    from tree_sitter import Language, Parser
    import tree_sitter_rust as tsr
    t = Parser(Language(tsr.language())).parse(out.encode())
    print()
    print("== expansion parses as valid Rust:", not t.root_node.has_error)
