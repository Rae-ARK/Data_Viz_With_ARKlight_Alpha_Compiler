"""
/playground content (PLAN.md Section 9).

Per-card expand/collapse data, one entry per framework, reusing
content.features.OUTPUT_MODEL_CARDS (the same copy already used on
/architecture) rather than inventing new text for the same claim --
(key, name, summary, detail, is_hero).

`key` is kept even though pages/playground.py's FrameworkCard no
longer needs it for a State(...) name (component(state=...), alpha
v0.062, namespaces each call site's state automatically) -- it's
still a stable, lowercase identifier useful as a dict/loop key
elsewhere, and dropping the tuple shape would be more diff than it's
worth for a field nothing else currently requires removing.
"""

from content.features import OUTPUT_MODEL_CARDS

PLAYGROUND_CARDS = [
    (name.lower(), name, summary, detail, is_hero)
    for name, summary, detail, is_hero in OUTPUT_MODEL_CARDS
]
