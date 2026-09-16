"""
Compatibility guard: this site uses alpha-branch-only ARKlight
features. See README.md ("Built against ARKlight's alpha branch") for
the full explanation and the correct install command.

Re-checked directly against a fresh clone of both branches at the
same point in time this project was last touched: alpha was at
v0.062, main at v0.54.0. Both now have `Site.style(...)` -- main
caught up on that one, so it's no longer what distinguishes them. The
feature that still doesn't exist on main at all (not even in
`arklight/api.py`, confirmed by grepping main's own source directly
rather than assumed from a stale table) is `component(...)`/`Prop`/
`ComponentState` -- the v0.060 "user-defined, reusable components"
milestone this project's /playground page now depends on
(component(state={...}), see pages/playground.py's FrameworkCard/
Counter). That's the guard's actual check now.

`Predicate`/`Show`/`Computed`/`Derive` (used on /bundle-size's budget
checker) exist in `arklight/api.py` on BOTH branches today, but,
confirmed directly, neither branch's `arklight/__init__.py`
re-exports them -- a real gap in ARKlight itself, not something this
guard can detect via `hasattr(Site(), ...)` or `import arklight`
alone, since `arklight.api.Predicate` etc. import fine either way.
Not guarded against here for that reason; pages/bundle_size.py and
pages/playground.py import them straight from `arklight.api` and
note the gap inline instead.

Kept as its own service module (not inline in site.py) because it's
infrastructure -- "can this even run" -- not site content or routing,
and the composition root should stay a thin list of route
registrations, not carry a multi-line diagnostic routine inline.
"""

from __future__ import annotations

_REQUIRED_FEATURES = ("component", "Prop", "ComponentState")  # v0.060, alpha-only


def check_arklight_compatibility() -> None:
    """Raise SystemExit with a clear message if ARKlight isn't alpha-branch-compatible."""
    import arklight

    installed_version = getattr(arklight, "__version__", "unknown")
    channel = getattr(arklight, "CHANNEL", None)
    missing = [f for f in _REQUIRED_FEATURES if not hasattr(arklight, f)]

    if missing:
        raise SystemExit(
            "\n"
            "This site requires ARKlight's 'alpha' branch --\n"
            f"it uses component(state={{...}}) (v0.060 'user-defined,\n"
            "reusable components'), which main doesn't have at all\n"
            "(confirmed against main's own arklight/api.py, not just its\n"
            "__init__.py exports).\n"
            f"Installed: version={installed_version!r}, channel={channel!r},\n"
            f"missing: {missing}.\n\n"
            "There is no working 'pip install arklight' path for this\n"
            "project -- install the alpha branch from source instead:\n\n"
            "    git clone --branch alpha https://github.com/Rae-ARK/ARKlight.git\n"
            "    cd ARKlight && pip install -e . "
            "--config-settings=yes-i-agree-to-arklight-license=1\n\n"
            "See this repo's README.md for the full compatibility table.\n"
        )
