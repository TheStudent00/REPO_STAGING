"""The inert hub for PseudoCoup version 5.

This version is the turn of the cycle where the hub is still empty.
The folder exists so the repo layout is the same across versions and
a version-to-version diff stays clean; what is in it is a surface
that REFUSES.

WHY IT REFUSES RATHER THAN DOING NOTHING
----------------------------------------
"Empty" has two possible spellings and only one of them is safe.

A surface whose names exist and quietly do nothing is the worse
failure this project keeps getting hurt by: transpiled code resolves
against it, runs, and produces wrong answers with nothing anywhere
reporting a problem. The bug surfaces later, far from its cause.

A surface whose names exist and raise on use is inert in the sense
that matters — it computes nothing — while being impossible to
mistake for a working hub. That is the same discipline already
settled elsewhere in the line: ingest records `unresolvable` honestly
and consumers halt on it, and PCv5's own TyCtxt stand-in was written
in a refusing style.

So: importing this module is fine, and touching anything in it is a
loud error naming exactly what was wanted.

WHY IT DECLARES NO NAMES OF ITS OWN
-----------------------------------
The hub's real surface is described in PseudoIR's plan and only
there, and it is not settled — the qualifier spelling is a
parser-level CPython fork where `r./` is a real token, and the
interim import-hook mechanism was dropped 2026-07-31 because it broke
debugger line numbers.

Writing a guessed list of names here would invent that surface in the
wrong repo. Instead this module answers to ANY name through
`__getattr__`, so whatever a transpiler emits gets a refusal that
names it. Nothing is invented and nothing is silently missing.

When PseudoIR delivers a real hub, it replaces this file. This is a
placeholder, not a design.
"""

__all__ = []

#: Where the real thing is defined, quoted in the error so a person
#: hitting this does not have to go looking.
_HUB_PLAN = "PRIVATE/PseudoIR/Planning/node_0_2_hub/CORE_0_2_hub.md"


class InertHubError(AttributeError, RuntimeError):
    """Raised on any use of the version 5 hub.

    Its own type so a caller that genuinely wants to detect "no hub
    yet" can catch this and nothing else — for instance a transpiler
    checking whether it is running in the hub-less turn of the cycle.

    IT SUBCLASSES BOTH, AND THAT IS LOAD-BEARING
    --------------------------------------------
    Found by this module's own test, 2026-07-31. A catch-all
    `__getattr__` refuses TOOLING INTROSPECTION as well as hub use.
    pytest asks every package for `pytest_plugins` before collecting
    it; the first version of this module raised on that question, and
    the whole test suite failed to collect with an error about the
    hub being inert — which was true, and useless.

    Python's introspection machinery — `hasattr`, `getattr` with a
    default, plugin discovery, debuggers, `dir()` — is written to
    treat AttributeError as "no such attribute" and carry on. So the
    error inherits from AttributeError, and those all behave
    normally again.

    It also inherits from RuntimeError, so a caller can still catch
    it as one, and so the name that shows in a traceback is
    InertHubError with its full message rather than a bare
    AttributeError that says nothing about why.

    The safety this appears to give up, it does not: transpiled code
    reaches a hub name by direct access — `hub.int64(...)` — which
    raises under either base class. Only `getattr(hub, x, default)`
    now returns the default quietly, and nothing emitted against a
    hub is written that way.
    """


def __getattr__(name):
    raise InertHubError(
        f"the version 5 hub is inert: nothing named {name!r} exists here, "
        f"and nothing here computes. this repo is the turn of the cycle "
        f"before a hub exists. the hub is described in {_HUB_PLAN} and is "
        f"built by PseudoIR; when it is delivered it replaces this module."
    )
