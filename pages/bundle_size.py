from __future__ import annotations

from arklight import (
    Action,
    Bind,
    Button,
    Container,
    Heading,
    Image,
    Prop,
    State,
    TableCell,
    TableRow,
    Text,
    component,
)

# `Predicate`/`Show`/`Computed`/`Derive` are implemented in
# arklight/api.py (alpha v0.062) but, confirmed directly, not
# re-exported from arklight/__init__.py -- see pages/playground.py's
# note on the same gap. Page-level State(...)/Computed(...) is fully
# supported for these (unlike component-owned state, see
# pages/playground.py's Counter() docstring), so this page is the
# right place to actually exercise them.
from arklight.api import Computed, Derive, Predicate, Show

from components.layout import page_shell
from components.meters import labeled_meter
from components.tables import data_table
from content.bundle_size import BUDGET_CHECK_TOOLS, BUNDLE_SIZE


@component(
    props={
        "label": Prop(),
        "size_state": Prop(),
        "overage_state": Prop(),
        "ratio_state": Prop(),
    },
)
def BudgetRow(label=None, size_state=None, overage_state=None, ratio_state=None):
    """
    One tool's row in the budget checker. Deliberately a plain
    `mode="macro"` component (no `state=` of its own) -- it only ever
    *reads* page-level State/Computed names handed in as props, which
    sidesteps the Show(...)-against-component-state gap documented on
    Counter() in pages/playground.py entirely, since every name here
    resolves to real page-level State(...)/Computed(...) by the time
    Show(...)/Bind(...) see it.
    """
    return Container(
        Text(label, class_name="muted"),
        # Bind(ratio_state) renders full float precision (e.g.
        # "3.3333333333333335x") -- checked `Derive.*`'s full
        # vocabulary (arklight/api.py: sum/multiply/subtract/divide/
        # min/max/join/format/count/uppercase/trim/compare) for a
        # rounding option before shipping this and there isn't one;
        # `Derive.format` is plain `{name}` substitution, not numeric
        # formatting. Left unrounded rather than faked with a
        # precomputed "clean" constant, since the point of this widget
        # is the live computation being real.
        Show(
            Predicate.gt("budget_kb", size_state),
            Text("Fits your budget -- ", Bind(ratio_state), "x under budget"),
        ),
        Show(
            Predicate.lt("budget_kb", size_state),
            Text("Over budget by ", Bind(overage_state), " KB"),
        ),
        Show(
            Predicate.equals("budget_kb", size_state),
            Text("Exactly at budget"),
        ),
        class_name="card",
    )


def _budget_checker():
    """
    Interactive "does this fit my JS budget" tool: State("budget_kb")
    adjustable +/-10 KB, Computed(...) per tracked tool using
    `Derive.subtract`/`Derive.divide` (both `v0.062` JS-vocabulary-
    addendum additions -- see ARKlight's CHANGELOG.md), and
    `Predicate.gt/lt/equals` (also `v0.062`) driving three mutually
    exclusive Show(...) branches per row via BudgetRow(...) above.

    All of State/Computed/Show/Predicate/Derive here are page-level,
    declared once and handed to page_shell's state= param -- the
    fully-supported path, unlike component-owned state (see
    pages/playground.py).
    """
    page_state = [State("budget_kb", 20)]
    rows = []
    for key, label, size_kb in BUDGET_CHECK_TOOLS:
        size_state = f"{key}_kb"
        overage_state = f"{key}_overage"
        ratio_state = f"{key}_ratio"
        page_state.append(State(size_state, size_kb))
        page_state.append(
            Computed(overage_state, deps=(size_state, "budget_kb"), derive=Derive.subtract(size_state, "budget_kb"))
        )
        # budget / size, not size / budget -- so a tool comfortably
        # under budget reads as e.g. "3.3x under budget" (>1), not a
        # sub-1 fraction. Caught by actually inspecting a build's
        # initial Bind(...) values (arklight_ratio came out 0.3 with
        # the operands reversed, for a tool that's well under budget),
        # not assumed correct from the Derive.divide call alone.
        page_state.append(
            Computed(ratio_state, deps=(size_state, "budget_kb"), derive=Derive.divide("budget_kb", size_state))
        )
        rows.append(BudgetRow(label=label, size_state=size_state, overage_state=overage_state, ratio_state=ratio_state))

    return page_state, Container(
        Heading("Budget checker", level=2),
        Text(
            "Set a JS budget, in KB, for your whole app and see which "
            "tools fit -- adjusted live via Computed(..., derive=Derive."
            "subtract/divide(...)), no page reload.",
            class_name="muted",
        ),
        Heading(Bind("budget_kb"), level=2, class_name="kpi-value"),
        Container(
            Button("-10", on_click=Action.decrement("budget_kb", 10), class_name="pill"),
            Button("Reset", on_click=Action.reset("budget_kb"), class_name="pill"),
            Button("+10", on_click=Action.increment("budget_kb", 10), class_name="pill"),
            class_name="cluster",
        ),
        Container(*rows, class_name="grid"),
        class_name="card",
    )


def bundle_size(theme: dict[str, str]):
    rows = [
        TableRow(
            TableCell(name),
            TableCell(f"{low} KB" if low == high else f"{low}-{high} KB"),
            TableCell(note, class_name="source-note"),
        )
        for name, low, high, note in BUNDLE_SIZE
    ]
    meters = [labeled_meter(name, (low + high) / 2, 0, 90) for name, low, high, _ in BUNDLE_SIZE]
    budget_state, budget_checker = _budget_checker()

    return page_shell(
        Heading("Bundle Size & Performance"),
        Text(
            "Every number below is gzipped JavaScript for a minimal app, "
            "before your own application code. Ranges reflect real "
            "disagreement across sources, not false precision.",
        ),
        Container(*meters, class_name="stack"),
        Heading("Full table", level=2),
        data_table(["Tool", "Gzipped JS", "Source"], rows),
        Image(
            src="assets/bundle-size-bar.png",
            alt="Bar chart: gzipped JavaScript for ARKlight, Svelte, Vue, React, and Angular",
            style={"max-width": "100%", "height": "auto"},
        ),
        budget_checker,
        title="Bundle Size & Performance",
        description="Gzipped JavaScript payload comparison: React, Vue, Svelte, Angular, and ARKlight.",
        theme=theme,
        state=budget_state,
    )
