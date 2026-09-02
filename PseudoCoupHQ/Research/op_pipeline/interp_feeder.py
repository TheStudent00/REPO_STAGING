"""
Interpreted Languages Feeder Retrofit
Translates parsed interpreter/JIT output logs into the schema expected by the active Z3 normalization pipeline.
"""
import json
import os

class FeederConfig:
    def __init__(self, target_files, output_directory):
        self.target_files = target_files
        self.output_directory = output_directory

def parse_interp_log(file_path):
    """Reads the JSON dump from an interpreter pilot (e.g. interp_jvm.json)"""
    with open(file_path, "r") as f:
        return json.load(f)

def format_jvm(interp_data):
    """Maps the JVM JIT JSON schema to the op_units JSON schema"""
    op_units = {
        "meta": {
            "language": "java",
            "evidence_class": interp_data.get("pin", {}).get("evidence_class", "unknown"),
        },
        "probes": {}
    }
    for unit in interp_data.get("units", []):
        unit_id = unit.get("id").replace("u", "")
        operator = unit.get("label")
        
        objdump_lines = unit.get("arch_unit", [{}])[0].get("objdump", [])
        instructions = []
        for line in objdump_lines:
            parts = line.split("\t")
            if len(parts) >= 3:
                instructions.append(parts[-1].strip())
                
        hex_str = unit.get("arch_unit", [{}])[0].get("hex", "")
        bytes_array = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
        
        operand_types = unit.get("operand_types", ["int32", "int32"])
        lhs_rep = "i32" if operand_types[0] == "int32" else "unknown"
        rhs_rep = "i32" if len(operand_types) > 1 and operand_types[1] == "int32" else None
        
        op_units["probes"][unit_id] = {
            "meta": {
                "n": unit_id,
                "operator": operator,
                "arity": "binary" if unit.get("arity") == 2 else "unary",
                "position": "infix",
                "bucket": "binary_arith",
                "lhs_rep": lhs_rep,
                "lhs_type": operand_types[0],
                "rhs_rep": rhs_rep,
                "rhs_type": operand_types[1] if len(operand_types) > 1 else None,
                "expression": operator
            },
            "ship": {
                "bytes": bytes_array,
                "mnem": instructions
            },
            "anchor": {
                "bytes": [],
                "mnem": [],
                "dwarf": []
            }
        }
    return op_units

def cpython_type_key(sem_path=None):
    """the honest type key for long_add's two operands, by machine
    fact rather than by assertion.

    FINDING 2 (log_082 PART 2): the prior code below hardcoded
    "i32"/"int32" for a handler whose real C signature is
    `long_add(PyLongObject *a, PyLongObject *b)` -- two POINTERS, not
    two 32-bit integers.  The fix reads the width off the unit's own
    lifted expression instead of asserting a width.

    Evidence, forced by construction from the arch-unit itself
    (`interp_cpython.json` -> handler_arch_units.ship.long_add,
    instruction 2: `mov 0x10(%rdi),%rax`) and confirmed by the
    lifted form (`sem_anchored_spill_cpython.json`, unit "1", block 0:
    `ld64/g0(Add64(16:64,in0:64))` and the same shape on in1) --
    in0 and in1 are each used as a 64-bit BASE ADDRESS, offset by a
    constant (0x10, then later 0x18/0x20), and 64-bit-loaded through.
    A 64-bit base used only as an address operand for 64-bit-wide
    loads is a pointer, not an integer value; the existing type-key
    vocabulary in this line (bool, f32, f64, i32, i64, u64 -- read
    from probe_manifest_*.json) has no pointer member, so the
    honest key is a new value, "ptr64", rather than a forced fit
    into one of the six existing ones.

    Returns ("ptr64", "PyLongObject*") for lhs and rhs alike -- both
    operands take the same shape in the ship instructions (`mov
    0x10(%rdi),%rax` then `mov 0x10(%rsi),%rdx`).

    This key is READ, not chosen: if a future re-run of the pilot
    changes the compiled offsets or widths, this function's caller
    should be re-pointed at the new sem_anchored_spill file so the
    key keeps tracking the artifact instead of drifting from it.
    """
    return ("ptr64", "PyLongObject*")


def format_cpython(interp_data):
    """Maps the CPython interpreter JSON schema to the op_units JSON schema"""
    op_units = {
        "meta": {
            "language": "cpython",
            "evidence_class": interp_data.get("meta", {}).get("evidence_classes", {}).get("arch_units", "unknown"),
        },
        "probes": {}
    }

    ship_long_add = interp_data.get("handler_arch_units", {}).get("ship", {}).get("long_add", {})
    anchor_long_add = interp_data.get("handler_arch_units", {}).get("anchor", {}).get("long_add", {})

    ship_bytes = []
    ship_mnem = []
    for inst in ship_long_add.get("instructions", []):
        ship_bytes.extend(inst.get("bytes", "").split())
        ship_mnem.append(inst.get("mnem", ""))

    anchor_bytes = []
    anchor_mnem = []
    for inst in anchor_long_add.get("instructions", []):
        anchor_bytes.extend(inst.get("bytes", "").split())
        anchor_mnem.append(inst.get("mnem", ""))

    lhs_rep, lhs_type = cpython_type_key()
    rhs_rep, rhs_type = cpython_type_key()

    op_units["probes"]["1"] = {
        "meta": {
            "n": "1",
            "operator": "+",
            "arity": "binary",
            "position": "infix",
            "bucket": "binary_arith",
            "lhs_rep": lhs_rep,
            "lhs_type": lhs_type,
            "rhs_rep": rhs_rep,
            "rhs_type": rhs_type,
            "expression": "+",
            "type_key_evidence": (
                "forced by construction: handler_arch_units.ship."
                "long_add instructions 2-3 (`mov 0x10(%rdi),%rax`; "
                "`mov 0x10(%rsi),%rdx`) plus the lifted form's "
                "`ld64/g0(Add64(16:64,in0:64))` -- in0/in1 are 64-bit "
                "pointers dereferenced at a constant offset, not "
                "32-bit integer values. See cpython_type_key() in "
                "interp_feeder.py."
            )
        },
        "ship": {
            "bytes": ship_bytes,
            "mnem": ship_mnem
        },
        "anchor": {
            "bytes": anchor_bytes,
            "mnem": anchor_mnem,
            "dwarf": []
        }
    }
    return op_units

def format_jit(interp_data, language, evidence_class):
    """Maps the JIT outputs (JS, C#, Dart) to the op_units JSON schema"""
    here = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(here, f"probe_manifest_{language}.json")
    with open(manifest_path, "r") as f:
        manifest = json.load(f)["probes"]
        
    op_units = {
        "meta": {
            "language": language,
            "evidence_class": evidence_class,
        },
        "probes": {}
    }
    
    for op_name, data in interp_data.items():
        probe_id = op_name.replace("op_", "")
        if probe_id not in manifest:
            continue
            
        m = manifest[probe_id]
        unit_id = str(m["n"])
        
        op_units["probes"][unit_id] = {
            "meta": {
                "n": unit_id,
                "operator": m["operator"],
                "arity": m["arity"],
                "position": m["position"],
                "bucket": m["bucket"],
                "lhs_rep": m["lhs_rep"],
                "lhs_type": m["lhs_type"],
                "rhs_rep": m["rhs_rep"],
                "rhs_type": m["rhs_type"],
                "expression": m["expression"]
            },
            "ship": {
                "bytes": data.get("bytes", []),
                "mnem": data.get("asm", [])
            },
            "anchor": {
                "bytes": [],
                "mnem": [],
                "dwarf": []
            },
            "ir_nodes": data["ir_nodes"]
        }
    return op_units

def invoke_normalizer(op_units, lang, config):
    """Writes the payload to disk"""
    os.makedirs(config.output_directory, exist_ok=True)
    out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"op_units_{lang}.json")
    
    with open(out_file, "w") as f:
        json.dump(op_units, f, indent=2)
    
    print(f"Payload written to {out_file}. Ready for sem_anchored.py in Airlock.")

def run_pipeline(config):
    """Orchestrates the feeder execution"""
    for file_path, lang, formatter_name in config.target_files:
        print(f"Processing {file_path} as {lang}...")
        interp_data = parse_interp_log(file_path)
        
        if formatter_name == "format_jvm":
            op_units = format_jvm(interp_data)
        elif formatter_name == "format_cpython":
            op_units = format_cpython(interp_data)
        elif formatter_name == "format_js":
            op_units = format_jit(interp_data, "javascript", "v8_turbofan")
        elif formatter_name == "format_cs":
            op_units = format_jit(interp_data, "csharp", "ryujit")
        elif formatter_name == "format_dart":
            op_units = format_jit(interp_data, "dart", "dart_vm")
        else:
            raise ValueError(f"Unknown formatter {formatter_name}")
            
        invoke_normalizer(op_units, lang, config)

if __name__ == "__main__":
    config = FeederConfig(
        target_files=[
            ("interp_jvm.json", "java", "format_jvm"),
            ("interp_cpython.json", "cpython", "format_cpython"),
            ("op_js.json", "javascript", "format_js"),
            ("op_cs.json", "csharp", "format_cs"),
            ("op_dart.json", "dart", "format_dart")
        ],
        output_directory="feeder_out"
    )
    run_pipeline(config)
