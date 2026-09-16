from __future__ import annotations

from arklight import Action, Bind, Button, Container, Heading, Prop, Text, component

from components.cards import card_class, card_grid
from components.layout import page_shell
from content.playground import PLAYGROUND_CARDS

# --------------------------------------------------------------------
# v0.060 "User-defined, reusable components" (shipped in full as of
# alpha v0.062 -- see docs/Foundational/USER-DEFINED-COMPONENTS.md)
# replaces the old hand-wired approach below: previously every
# expand/collapse card needed its own State(f"show_detail_{key}", ...)
# declared up at page_shell's state= param, plumbed through a `key`
# string threaded from content/playground.py just to keep each card's
# name collision-free. component(state={...}) does that hoisting
# itself now -- every FrameworkCard(...) call site gets its own
# independent, instance-scoped "open" value with zero manual plumbing,
# confirmed directly against the Stage 4 implementation (each instance
# is namespaced onto the page under a unique key at expansion time,
# before Validation ever runs).
# --------------------------------------------------------------------


@component(
    props={
        "name": Prop(),
        "summary": Prop(),
        "detail": Prop(),
        "is_hero": Prop(default=False),
    },
    state={"open": False},
)
def FrameworkCard(name=None, summary=None, detail=None, is_hero=False):
    return Container(
        Heading(name, level=3),
        Text(summary, class_name="muted"),
        Button("Toggle details", on_click=Action.toggle_bool("open"), class_name="pill"),
        Container(
            Text(detail),
            class_name="playground-panel",
            bind_class=Bind.when("open", "playground-panel-open"),
        ),
        class_name=card_class(is_hero=is_hero),
    )


@component(
    props={"label": Prop(default="Live counter"), "start": Prop(default=0)},
    state={"count": 0, "milestone": 5},
)
def Counter(label="Live counter", start=0):
    """
    Two independent `Counter()` instances appear on this page (see
    playground() below) specifically to demonstrate what "instance-
    scoped" component state actually means in practice: each one owns
    its own "count"/"milestone" pair, so clicking one's buttons never
    touches the other's readout -- verified directly against a build
    with two instances side by side, not assumed from the docs alone.

    `milestone` is declared but deliberately unused by any Show(...)
    here -- tried first, and reverted after an actual build error:
    `_rewrite_component_state_refs` (arklight/ir/components.py, v0.060
    Stage 4) only retargets `Bind(...)`/`Action.*(...)`/`bind_class=`/
    `bind_value=` references onto a component instance's namespaced
    state key -- exactly the four kinds
    docs/Foundational/USER-DEFINED-COMPONENTS.md's "Component-owned
    state" section lists as working, and no more. A `Show(Predicate.gt(
    "count", "milestone"))` inside this same render function fails the
    real build with "references state 'count', which isn't declared on
    this page" -- Show/Predicate against component-owned state isn't
    (yet) one of the rewritten reference kinds, confirmed by actually
    building it, not inferred from the docs' silence on the point. See
    pages/bundle_size.py for `Predicate.gt` used against page-level
    State(...) instead, where it's fully supported.
    """
    return Container(
        Heading(label, level=3),
        Heading(Bind("count"), level=2, class_name="kpi-value"),
        Container(
            Button("-1", on_click=Action.decrement("count"), class_name="pill"),
            Button("Reset", on_click=Action.reset("count"), class_name="pill"),
            Button("+1", on_click=Action.increment("count"), class_name="pill"),
            class_name="cluster",
        ),
        class_name="card",
    )


def playground(theme: dict[str, str]):
    cards = card_grid(*[FrameworkCard(name=name, summary=summary, detail=detail, is_hero=is_hero)
                         for _key, name, summary, detail, is_hero in PLAYGROUND_CARDS])

    return page_shell(
        Heading("Playground"),
        Text(
            "Everything on this page is real, compiled State/Bind/"
            "Action interactivity -- not a mockup. Every card and both "
            "counters below are the SAME component (FrameworkCard/"
            "Counter, component(state=...)) called multiple times; "
            "each call gets its own independent state, wired up "
            "automatically rather than hand-declared per instance.",
        ),
        Heading("Framework cards -- independent expand/collapse", level=2),
        cards,
        Heading("Counters -- independent instance-scoped state", level=2),
        Text(
            "Two calls to the same Counter(...) component. Watch how "
            "incrementing one never moves the other.",
            class_name="muted",
        ),
        Container(
            Counter(label="Counter A", start=0),
            Counter(label="Counter B", start=0),
            class_name="grid",
        ),
        title="Playground",
        description="A live component(state=...) demo -- expandable cards and two independent counters, running entirely on ARKlight's closed-vocabulary JS runtime.",
        theme=theme,
    )
