"""Cache mounted code keyed by (intention, language, type-tuple, plan-identity) so a plan change invalidates it.

PROVENANCE (harvested pattern, adapted):
  The (operation, type) cache-key shape is the PCv5 dispatch pattern from
  <WORKSPACE_DIR>/PseudoCoup_v5/Research/rust_routing/pc_runtime.py +
  ledger.py (read-and-verified): the ledger answers the operand-type
  question, and the mounted routine is chosen by (bin_op, ty). PCv5 held
  mounted pages for process life via that dispatch.

ADDED in PCv6 (marked as new):
  - The plan's identity is part of the key, so re-planning a slice
    invalidates (closes and re-mounts) the stale executable page instead
    of silently reusing code compiled from an older plan.
  - Lifetime is kept (hold for process life) but made EXPLICIT and
    MEASURABLE: `live()` reports how many logical slots hold a page, and
    page release is observable through mount_bytes.live_pages().
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from mount_bytes import FN2, mount, MountTarget, live_pages   # noqa: E402


class InsertionCache:
    """Process-lifetime cache of mounted code; a changed plan-identity for a slot evicts the old page."""

    def __init__(self):
        # logical slot key -> (plan_identity, MountedCode)
        self._slots = {}

    @staticmethod
    def _logical_key(intention, language, type_tuple):
        return (intention, language, tuple(type_tuple))

    def get_or_mount(self, intention, language, type_tuple, plan_identity,
                     code, sig=FN2, target=MountTarget()):
        """Return the mounted code for this slot, (re)mounting if the plan changed.

        A different `plan_identity` for the same (intention, language,
        type-tuple) closes the stale page (invalidation) before mounting
        the new bytes."""
        key = self._logical_key(intention, language, type_tuple)
        existing = self._slots.get(key)
        if existing is not None:
            old_plan, mounted = existing
            if old_plan == plan_identity:
                return mounted                      # hot: reuse held page
            mounted.close()                         # plan changed -> release stale page
        m = mount(code, sig, target)
        self._slots[key] = (plan_identity, m)
        return m

    def plan_for(self, intention, language, type_tuple):
        """The plan-identity currently mounted for a slot, or None."""
        existing = self._slots.get(self._logical_key(intention, language, type_tuple))
        return None if existing is None else existing[0]

    def live(self) -> int:
        """How many logical slots currently hold a mounted page."""
        return len(self._slots)

    def live_pages(self) -> int:
        """Live executable pages process-wide (proxy to mount_bytes accounting)."""
        return live_pages()

    def close_all(self):
        """Release every held page (makes leak-free teardown explicit)."""
        for _plan, mounted in self._slots.values():
            mounted.close()
        self._slots.clear()
