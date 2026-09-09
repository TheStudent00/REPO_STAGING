# log 122 — the swift source, obtained in one command

Date: 2026-09-01. Follows log 121 §1's open item ("no swift
compiler source is checked out") and the owner's account of a chat that
treated obtaining it as a hard problem. It is not one, and the
proof is that it is now on disk.

## 1. What was done

- The toolchain pin: swift 6.0.3 (toolchain skill, the Airlock
  interpreter table: `/persist/swift/usr/bin/swift`, 6.0.3).
- One command, from the sandbox, through the ordinary proxy:

```
    git clone --depth 1 --branch swift-6.0.3-RELEASE \
        https://github.com/swiftlang/swift.git
```

- Wall time under two minutes, 292 MB shallow. Verified at the
  pin, the tool's own testimony:

```
    $ git log -1 --format="%H %s"
    6a862d2eb7128ff1f317b07e8ad1a6da939775f3
        Change version string to 'swift-6.0.3-RELEASE'
```

## 2. Where it lives

- `Sources/swift-6.0.3-RELEASE/` — beside
  llvm-project, golang_src, rust, jdk, graal, matching the
  existing convention of pinned sources under Sources/.
- The type-authority files log 121 route (c) wanted are present,
  e.g. `stdlib/public/core/Integers.swift`, `Bool.swift`,
  `FloatingPointTypes.swift.gyb`.
- HOUSEKEEPING NOTE: `Sources/swift/` is a STALE,
  BROKEN partial clone (a .git with no commits) left by an
  earlier attempt; the sandbox cannot unlink its lock files.
  the owner can delete the directory from the host. Nothing reads it.

## 3. For the record, per log 121's own routes

- Route (c) — clone at the tag matching the pin — is the route
  taken, and it cost one command. Routes (a)/(b) (installed
  stdlib interface files; swiftc emitting the module interface)
  remain valid cross-witnesses for the type inventory and are
  cheaper still where only the type list is needed.
- The task-29 follow-on this unblocks: swift's extracted type
  authority, read from these sources at this pin, closing the one
  hole in type_inventory.json.
