"""PLAN.md Section 2a -- gzipped JS, minimal app (KB)."""

BUNDLE_SIZE = [
    # (name, low_kb, high_kb, note)
    ("ARKlight (static page)", 0.5, 0.5, "Measured this session -- no State() declared"),
    ("ARKlight (with State/Bind/Action)", 5.98, 5.98, "Measured this session -- vendored vdom core included"),
    ("Svelte 5", 1.6, 5.0, "State of JS 2025 / 2026 benchmark roundups"),
    ("Vue 3/4", 16.0, 35.0, "Vue perf docs / 2026 comparisons"),
    ("React 19 + ReactDOM", 42.0, 48.0, "js-framework-benchmark / 2026 sources"),
    ("Angular (core)", 50.0, 80.0, "2026 Angular performance roundups"),
]

# pages/bundle_size.py's interactive "Budget checker" widget -- one
# entry per tool it tracks, (state_key, display_label, mid_kb). Kept
# as its own small list rather than reusing BUNDLE_SIZE directly
# because `state_key` has to be a clean, unique Python-identifier-ish
# token (it becomes `f"{key}_kb"`/`f"{key}_overage"`/`f"{key}_ratio"`
# State/Computed names), which BUNDLE_SIZE's free-text `name` strings
# (e.g. "ARKlight (with State/Bind/Action)") aren't. `mid_kb` is each
# tool's BUNDLE_SIZE range midpoint, rounded to one decimal.
BUDGET_CHECK_TOOLS = [
    ("arklight", "ARKlight (interactive page)", 6.0),
    ("svelte", "Svelte 5", 3.3),
    ("vue", "Vue 3/4", 25.5),
    ("react", "React 19 + ReactDOM", 45.0),
    ("angular", "Angular (core)", 65.0),
]
