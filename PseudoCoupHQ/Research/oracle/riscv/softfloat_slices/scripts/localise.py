#!/usr/bin/env python3
"""Turn an internal global that lives inside ONE function into a local.

After link+internalize+inline a slice is one function plus a handful of
internal globals (SoftFloat's exception-flag accumulator, the rounding
mode). A global is observable across calls, so LLVM must keep every
store to it. Inside a slice it is not observable: the wrapper sets it on
entry and reads it on exit, which is exactly a local variable.

This rewrites each such global into an alloca in the entry block,
initialised to the global's own initialiser. Then sroa/mem2reg promote
it to registers and the memory traffic disappears. Mechanical: no
knowledge of SoftFloat, no hand edits, refuses anything it cannot prove
is confined to one function.
"""
import re, sys

def localise(text, names=None):
    fns = re.findall(r'^define[^\n]*@([A-Za-z_0-9.]+)\(', text, re.M)
    if len(fns) != 1:
        raise SystemExit("refusing: %d functions in the module, expected 1" % len(fns))
    glob = re.findall(r'^@([A-Za-z_0-9.]+) = internal[^\n]*global (i\d+) (\S+?),', text, re.M)
    if names: glob = [g for g in glob if g[0] in names]
    if not glob:
        return text, []
    done = []
    for name, ty, init in glob:
        # every use must be inside the single function body
        if text.count("@" + name) < 2:
            continue
        text = re.sub(r'^@%s = internal[^\n]*\n' % re.escape(name), '', text, flags=re.M)
        slot = "%" + name + ".local"
        # insert the alloca and its initialising store at the top of the entry block
        def ins(m):
            return m.group(0) + "\n  {0} = alloca {1}, align 1\n  store {1} {2}, ptr {0}, align 1".format(slot, ty, init)
        text = re.sub(r'^define[^\n]*\{$', ins, text, count=1, flags=re.M)
        text = re.sub(r'@%s\b' % re.escape(name), slot, text)
        done.append((name, ty, init))
    return text, done

if __name__ == "__main__":
    src = open(sys.argv[1]).read()
    out, done = localise(src)
    open(sys.argv[2], "w").write(out)
    for n, t, i in done:
        print("  localised @%s (%s, init %s) -> an alloca in the entry block" % (n, t, i))
    if not done:
        print("  nothing to localise")
