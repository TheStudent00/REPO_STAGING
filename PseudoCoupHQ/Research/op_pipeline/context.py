"""context.py -- hq.research.compiler_graph.arch_unit.context

The owed data of the `context` node: a body that names a constant by a
relocation (`!!reloc=R_X86_64_PC32:.LCPI0_0-0x4`) or by a rip-relative
offset does not carry the constant's BYTES anywhere.  This reads them.

Route, and why it is the strongest available:

  1. the unit's own probe source is read out of the probe manifest the
     lane generated (probe_manifest_<lang>.json for the original
     population, probe_manifest2_<lang>.json for the regenerated one);
  2. the SHIP build is repeated with the lane's own flags
     (lanes/op_asg_<lang>.sh, compile_probe);
  3. the rebuilt body's bytes are compared with the bytes recorded on
     the unit.  A unit whose bytes do not match is REFUSED -- its
     constant is not written down on a guess;
  4. the constant is read out of the object with objdump and readelf,
     the tools' own printing, never computed by this file.

Output: canon39_context.json, a NEW sidecar.  No canon39_* file is
edited.

Run:  python3 context.py <lang> [<lang> ...]      (writes one part file)
      python3 context.py --join                   (writes the sidecar)
"""

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PART = "canon39_context_part_%s.json"
OUT = "canon39_context.json"

CLANG = "clang"
CLANGXX = "clang++"

RIP = re.compile(r"\(%rip\)")
RELOC = re.compile(r"!!reloc=R_X86_64_\w+:([^\s;]+?)(?:[-+]0x[0-9a-f]+)?(?=$|;|\s)")

# how many bytes an instruction reads at a rip-relative site.  Used only
# where no symbol bounds the constant (go's linked binary has no local
# symbol at the site).
ACCESS = {
    "movss": 4,
    "movsd": 8,
    "movd": 4,
    "movq": 8,
    "movaps": 16,
    "movapd": 16,
    "movups": 16,
    "movupd": 16,
    "xorps": 16,
    "xorpd": 16,
    "andps": 16,
    "andpd": 16,
    "orps": 16,
    "orpd": 16,
    "subpd": 16,
    "addpd": 16,
    "mulpd": 16,
    "pxor": 16,
}


def sh(cmd, cwd=None, timeout=300, env=None):
    p = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    return p.returncode, p.stdout, p.stderr


def load_units():
    """every unit of the corpus whose body carries a rip-relative site."""
    rows = []
    names = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        names.append("canon39_wrapped_%s.json" % lang)
    store = os.path.join(HERE, "canon39_regen_store")
    for name in sorted(os.listdir(store)):
        if name.endswith(".json"):
            names.append(os.path.join("canon39_regen_store", name))
    for name in names:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        doc = json.load(open(path))
        for uid, unit in (doc.get("units") or {}).items():
            text = unit.get("body_text") or ""
            if not RIP.search(text):
                continue
            rows.append({
                "unit": uid,
                "lang": unit.get("lang") or uid.split("/")[0],
                "population": unit.get("population") or "original",
                "n": unit.get("n"),
                "body_text": text,
                "body_bytes": unit.get("body_bytes") or "",
            })
    return rows


def manifest_source(lang, population, n):
    stem = "probe_manifest2_" if population == "regenerated" else "probe_manifest_"
    path = os.path.join(HERE, stem + lang + ".json")
    if not hasattr(manifest_source, "cache"):
        manifest_source.cache = {}
    if path not in manifest_source.cache:
        if not os.path.exists(path):
            manifest_source.cache[path] = None
        else:
            doc = json.load(open(path))
            probes = doc.get("probes") or {}
            if isinstance(probes, list):
                by_n = {}
                for p in probes:
                    by_n[str(p.get("n"))] = p
                probes = by_n
            manifest_source.cache[path] = probes
    probes = manifest_source.cache[path]
    if probes is None:
        return None, "no probe manifest on disk at %s" % (stem + lang + ".json")
    probe = probes.get(str(n))
    if not probe:
        return None, "the probe manifest has no row for probe %s" % n
    return probe, None


def build_ship(lang, source, work):
    """the lane's own ship build, repeated.  (object path, symbol, cause)"""
    if lang == "c":
        src = os.path.join(work, "unit.c")
        obj = os.path.join(work, "unit_ship.o")
        open(src, "w").write(source)
        rc, so, se = sh([CLANG, "-std=c17", "-O1", "-c", src, "-o", obj])
        if rc != 0:
            return None, (se or so)
        return obj, None
    if lang == "cpp":
        src = os.path.join(work, "unit.cpp")
        obj = os.path.join(work, "unit_ship.o")
        open(src, "w").write(source)
        rc, so, se = sh([CLANGXX, "-std=c++20", "-O1", "-c", src, "-o", obj])
        if rc != 0:
            return None, (se or so)
        return obj, None
    if lang == "rust":
        src = os.path.join(work, "unit.rs")
        obj = os.path.join(work, "unit_ship.o")
        open(src, "w").write(source)
        cmd = ["rustc", "--crate-type=lib", "--emit=obj"]
        cmd += ["-C", "opt-level=1", "-C", "debug-assertions=off"]
        cmd += ["-o", obj, src]
        rc, so, se = sh(cmd)
        if rc != 0:
            return None, (se or so)
        return obj, None
    if lang == "go":
        open(os.path.join(work, "go.mod"), "w").write(
            "module opprobe\n\ngo 1.26\n")
        open(os.path.join(work, "main.go"), "w").write(source)
        obj = os.path.join(work, "bin_ship")
        env = dict(os.environ)
        env["GOTOOLCHAIN"] = "local"
        env["GOPROXY"] = "off"
        env["GOFLAGS"] = "-mod=mod"
        env["GOCACHE"] = os.path.join(work, "gocache")
        env["GOPATH"] = os.path.join(work, "gopath")
        env["HOME"] = work
        rc, so, se = sh(["go", "build", "-o", obj, "."], cwd=work, env=env)
        if rc != 0:
            return None, (se or so)
        return obj, None
    if lang == "swift":
        return None, ("swiftc is not installed on this machine; the lane built "
                      "swift with /persist/swift/usr/bin/swiftc inside the "
                      "Airlock image")
    return None, "no ship build is written for %s" % lang


def disassemble(obj, symbol):
    rc, so, se = sh(["objdump", "-dr", "--disassemble=" + symbol, obj])
    if rc != 0:
        return None, se or so
    return so, None


def flat_bytes(dump):
    """objdump's own byte column, flattened, in order."""
    out = []
    for line in dump.splitlines():
        m = re.match(r"^\s+[0-9a-f]+:\t([0-9a-f ]+?)(?:\t|\s*$)", line)
        if m:
            out.extend(m.group(1).split())
    return " ".join(out)


def section_table(obj):
    """readelf's own section list, in ELF section-index order, so that a
    symbol's section index names the same section the linker meant."""
    rc, so, se = sh(["readelf", "-SW", obj])
    rows = []
    for line in so.splitlines():
        m = re.match(
            r"^\s*\[\s*(\d+)\]\s+(\S*)\s+(\S+)\s+([0-9a-f]+)\s+([0-9a-f]+)"
            r"\s+([0-9a-f]+)", line)
        if not m:
            continue
        index = int(m.group(1))
        while len(rows) < index:
            rows.append({"name": "", "size": 0, "vma": 0})
        rows.append({
            "name": m.group(2),
            "vma": int(m.group(4), 16),
            "size": int(m.group(6), 16),
        })
    return rows


def symbols(obj):
    rc, so, se = sh(["readelf", "-sW", obj])
    rows = []
    for line in so.splitlines():
        parts = line.split()
        if len(parts) >= 8 and parts[0].endswith(":"):
            try:
                value = int(parts[1], 16)
            except ValueError:
                continue
            rows.append({
                "value": value,
                "size": int(parts[2]) if parts[2].isdigit() else 0,
                "ndx": parts[6],
                "name": parts[7],
            })
    return rows


def section_bytes(obj, name):
    rc, so, se = sh(["objdump", "-s", "-j", name, obj])
    hexes = []
    for line in so.splitlines():
        m = re.match(r"^\s+([0-9a-f]+)\s((?:[0-9a-f]{2,8} ){1,4})", line)
        if m:
            hexes.append(m.group(2).replace(" ", ""))
    return "".join(hexes)


def spaced(hexstr):
    return " ".join(hexstr[i:i + 2] for i in range(0, len(hexstr), 2))


def sites_of(body_text):
    """one entry per rip-relative site, in body order."""
    out = []
    for step in body_text.split("; "):
        if "(%rip)" not in step:
            continue
        mnem = step.split()[0]
        m = RELOC.search(step)
        out.append({
            "site": step,
            "mnem": mnem,
            "symbol": m.group(1) if m else None,
        })
    return out


def bytes_for_symbol(obj, symbol, sects, syms):
    """the symbol's bytes, and its extent, read off the object."""
    here = None
    for s in syms:
        if s["name"] == symbol:
            here = s
            break
    if here is None:
        return None, None, None, "no symbol named %s in the rebuilt object" % symbol
    ndx = here["ndx"]
    if ndx == "UND":
        return None, None, None, (
            "%s is an undefined symbol -- the site reaches a routine, not a "
            "constant, and a routine is the callees part of the record"
            % symbol)
    try:
        sect = sects[int(ndx)]
    except (ValueError, IndexError):
        return None, None, None, "symbol %s names section index %s, which is not a section" % (symbol, ndx)
    end = sect["size"]
    for s in syms:
        if s["ndx"] == ndx and s["value"] > here["value"] and s["value"] < end:
            end = s["value"]
    width = end - here["value"]
    if here["size"]:
        width = here["size"]
    raw = section_bytes(obj, sect["name"])
    chunk = raw[here["value"] * 2:(here["value"] + width) * 2]
    if not chunk:
        return None, None, sect["name"], "section %s printed no bytes at offset %d" % (sect["name"], here["value"])
    return spaced(chunk), width, sect["name"], None


def bytes_at_address(obj, addr, width, sects):
    for sect in sects:
        if sect["vma"] and sect["vma"] <= addr < sect["vma"] + sect["size"]:
            raw = section_bytes(obj, sect["name"])
            off = addr - sect["vma"]
            chunk = raw[off * 2:(off + width) * 2]
            if not chunk:
                return None, sect["name"], "section %s printed no bytes at 0x%x" % (sect["name"], addr)
            return spaced(chunk), sect["name"], None
    return None, None, "no section of the rebuilt binary holds address 0x%x" % addr


TARGET = re.compile(r"^\s+([0-9a-f]+):\t[0-9a-f ]+\t(\S+)[^#]*#\s*([0-9a-f]+)")


def go_targets(dump):
    """objdump's own `# <addr>` note at each rip-relative site."""
    out = []
    for line in dump.splitlines():
        if "(%rip)" not in line:
            continue
        m = TARGET.match(line)
        if m:
            out.append({"mnem": m.group(2), "addr": int(m.group(3), 16)})
    return out


def one_unit(row):
    lang = row["lang"]
    probe, cause = manifest_source(lang, row["population"], row["n"])
    if probe is None:
        return {"unit": row["unit"], "cause": cause}
    symbol = probe.get("symbol") or ""
    work = tempfile.mkdtemp(prefix="context_")
    try:
        obj, cause = build_ship(lang, probe.get("source") or "", work)
        if obj is None:
            first = ((cause or "").strip().splitlines() or [""])[0]
            return {"unit": row["unit"],
                    "cause": "the ship build did not run: " + first}
        dump, cause = disassemble(obj, symbol)
        if dump is None:
            return {"unit": row["unit"],
                    "cause": "objdump could not disassemble %s: %s" % (symbol, cause)}
        rebuilt = flat_bytes(dump)
        recorded = row["body_bytes"]
        same = rebuilt == recorded
        sects = section_table(obj)
        syms = symbols(obj)
        entries = []
        missing = []
        if lang == "go":
            targets = go_targets(dump)
            for i, site in enumerate(sites_of(row["body_text"])):
                width = ACCESS.get(site["mnem"])
                if i >= len(targets):
                    missing.append("site %d: objdump printed no target address" % i)
                    continue
                addr = targets[i]["addr"]
                if width is None:
                    missing.append(
                        "site %d (%s): the body takes this address, it reads no "
                        "value of a stated width" % (i, site["mnem"]))
                    continue
                data, sect, cause = bytes_at_address(obj, addr, width, sects)
                if data is None:
                    missing.append("site %d: %s" % (i, cause))
                    continue
                entries.append({
                    "symbol": "0x%x" % addr,
                    "bytes": data,
                    "width": width,
                    "section": sect,
                    "site": site["site"],
                    "read_with": "objdump -s -j %s" % sect,
                })
        else:
            for i, site in enumerate(sites_of(row["body_text"])):
                if not site["symbol"]:
                    missing.append(
                        "site %d (%s): the body names no relocation at this site"
                        % (i, site["mnem"]))
                    continue
                data, width, sect, cause = bytes_for_symbol(
                    obj, site["symbol"], sects, syms)
                if data is None:
                    missing.append("site %d: %s" % (i, cause))
                    continue
                entries.append({
                    "symbol": site["symbol"],
                    "bytes": data,
                    "width": width,
                    "section": sect,
                    "site": site["site"],
                    "read_with": "readelf -sW + objdump -s -j %s" % sect,
                })
        record = {
            "unit": row["unit"],
            "lang": lang,
            "population": row["population"],
            "context": entries,
            "sites": len(sites_of(row["body_text"])),
            "rebuilt_body_bytes_match_the_record": same,
            "built_with": "the lane's own ship flags, repeated on this machine",
        }
        if not same:
            record["context"] = []
            record["cause"] = (
                "the rebuilt body's bytes differ from the bytes recorded on "
                "the unit, so no constant of this rebuild is written down")
        elif missing:
            record["sites_with_no_bytes"] = missing
        return record
    finally:
        pass


def run(langs):
    rows = load_units()
    for lang in langs:
        mine = [r for r in rows if r["lang"] == lang]
        out = {}
        for row in mine:
            out[row["unit"]] = one_unit(row)
        path = os.path.join(HERE, PART % lang)
        json.dump({"lang": lang, "units": out}, open(path, "w"),
                  indent=1, sort_keys=True)
        got = 0
        for r in out.values():
            if r.get("context"):
                got += 1
        print("%s: %d units carry a rip-relative site, %d got their bytes"
              % (lang, len(mine), got))


def join():
    rows = load_units()
    units = {}
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        path = os.path.join(HERE, PART % lang)
        if not os.path.exists(path):
            continue
        units.update(json.load(open(path))["units"])
    with_bytes = 0
    without = {}
    sites = 0
    for uid, rec in units.items():
        sites += rec.get("sites", 0)
        if rec.get("context"):
            with_bytes += 1
        else:
            without[uid] = rec.get("cause") or (
                rec.get("sites_with_no_bytes") or ["no cause recorded"])[0]
    doc = {
        "meta": {
            "node": "hq.research.compiler_graph.arch_unit.context",
            "generated_by": "context.py",
            "population": (
                "every arch-unit of the corpus whose body carries a "
                "rip-relative site, over all 31,078 units"),
            "how": (
                "the probe source is read from the probe manifest, the "
                "lane's own ship build is repeated on this machine, the "
                "rebuilt body's bytes are compared with the bytes recorded "
                "on the unit, and the constant is read with readelf -sW and "
                "objdump -s -j <section>"),
            "note": (
                "a sidecar: no canon39_* file is edited.  The unit id is the "
                "only key; nothing here is grouped or paired."),
        },
        "tally": {
            "units_with_a_rip_relative_site": len(rows),
            "units_with_their_bytes": with_bytes,
            "units_without_their_bytes": len(without),
            "rip_relative_sites": sites,
        },
        "units": units,
        "units_without_bytes_and_why": without,
    }
    path = os.path.join(HERE, OUT)
    json.dump(doc, open(path, "w"), indent=1, sort_keys=True)
    print(json.dumps(doc["tally"], indent=1))
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(path)))


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
    elif args[0] == "--join":
        join()
    else:
        run(args)
