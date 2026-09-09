"""Acceptance test for the inert hub.

Standing project rule: every tool ships with its own acceptance test.
The hub is not a tool, but "inert" is a claim, and an unchecked claim
about code is worth nothing.

Run:  python3 -m pytest PseudoCoup_v5/hub -q
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hub  # noqa: E402


def test_importing_is_fine():
    """Import must NOT raise. A transpiler has to be able to name the
    hub without touching it — otherwise the refusal fires at import
    time and says nothing about which name was wanted."""
    assert hub is not None


def test_any_name_refuses():
    """The surface is undeclared on purpose, so every name refuses —
    not just a guessed list of them."""
    for name in ("int64", "bool", "list", "map", "anything_at_all"):
        with pytest.raises(hub.InertHubError):
            getattr(hub, name)


def test_the_refusal_names_what_was_wanted():
    """A refusal that does not say what was asked for makes the caller
    guess, which is how a missing name turns into an afternoon."""
    with pytest.raises(hub.InertHubError) as caught:
        hub.some_operator
    assert "some_operator" in str(caught.value)


def test_the_refusal_says_where_the_real_hub_is_defined():
    with pytest.raises(hub.InertHubError) as caught:
        hub.whatever
    assert "PseudoIR" in str(caught.value)


def test_the_error_is_catchable_on_its_own_type():
    """So a caller can detect the hub-less turn of the cycle
    deliberately, rather than by catching everything."""
    with pytest.raises(hub.InertHubError):
        hub.x
    assert issubclass(hub.InertHubError, RuntimeError)


def test_introspection_does_not_explode():
    """Regression, 2026-07-31. The first version of this module made
    the refusal a plain RuntimeError, so pytest asking the package for
    `pytest_plugins` raised, and the entire suite failed to COLLECT
    with an error about the hub being inert.

    Tools ask packages questions. A question must get an answer, not a
    refusal — otherwise the inert hub breaks every tool that walks the
    repo, which is a much worse problem than the one it solves."""
    assert not hasattr(hub, "pytest_plugins")
    assert getattr(hub, "anything", "fallback") == "fallback"
    dir(hub)


def test_direct_access_still_raises_despite_that():
    """The concession above must not have made it quiet. Transpiled
    code reaches a hub name by direct attribute access, and that is
    the path that has to stay loud."""
    with pytest.raises(hub.InertHubError):
        hub.int64
