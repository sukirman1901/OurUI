# Component authoring

Reuse UI with **function components** or **`Component` classes**. Both expand at analyze time into built-in `ui.*` nodes before lowering to HTML.

```python
from ourui import Component, ui

def FeatureCard(title: str):
    return ui.Card(title)

class Banner(Component):
    def __init__(self, text: str):
        self.text = text

    def build(self):
        return ui.Section(title=self.text)

page = ui.Page(
    FeatureCard("Analysis"),
    Banner("Class component"),
)
```

Normative rules: [Language Spec — Components](../../../LANGUAGE_SPEC.md#components-phase-i).

## Function components

A function component is a plain Python function that takes props and **returns a single `ui.*` call** (or nested component call):

```python
def FeatureCard(title: str):
    return ui.Card(title)

def PricingRow(label: str, price: str):
    return ui.Section(
        title=label,
        children=[ui.Text(price)],
    )
```

Use it like any other node:

```python
page = ui.Page(
    FeatureCard("Analysis"),
    PricingRow("Pro", "$29/mo"),
)
```

Detection: any module-level function whose body is a single `return` of a `ui.*` or component call (and that is not decorated with `@server`) is treated as a component.

Optional: decorate with `@component` from `ourui` to mark intent explicitly — auto-detection works without it.

## Class components

Subclass **`Component`**, store props on `self` (typically in `__init__`), and implement **`build()`** returning the UI tree:

```python
from ourui import Component, ui

class CounterPanel(Component):
    def __init__(self, label: str):
        self.label = label

    def build(self):
        return ui.Section(
            title=self.label,
            children=[
                ui.Text(count),
                ui.Button("+1", color="primary", on_click=increment),
            ],
        )
```

Instantiate inside a page:

```python
page = ui.Page(CounterPanel("Counter"))
```

Parameter binding:

- **`__init__` parameters** (except `self`) become props when present
- If there is no `__init__`, **`build()` parameters** (except `self`) are used
- Inside `build()`, reference init props as **`self.prop_name`**

## Expansion and provenance

Components expand **before IIR**. Nested component calls expand recursively (depth limit 16). Provenance records the expansion chain, for example `expand:FeatureCard`.

The body must return **one** UI root — a `ui.*` call or another component that eventually lowers to `ui.*`.

## When to use which

| Style | Good for |
|-------|----------|
| Function | Leaf widgets, simple prop → UI mapping |
| Class | Clear object boundary, init-time setup, larger `build()` trees |

Both compose identically inside `ui.Page`, `ui.Section`, and other containers.

## What is not a component

These are **not** expanded as UI components:

- Functions decorated with **`@server`** — registered as RPC handlers instead
- Functions that do not return a single `ui.*` / component call
- Arbitrary Python classes that do not subclass **`Component`**

## Full example

See `examples/tutorial/02_components.py` and `examples/tutorial/06_counter_app.py`:

```python
from ourui import Component, State, server, ui

count = State(0)

@server
def increment() -> int:
    count.set(count.get() + 1)
    return count.get()

def FeatureCard(title: str):
    return ui.Card(title)

class CounterPanel(Component):
    def __init__(self, label: str):
        self.label = label

    def build(self):
        return ui.Section(
            title=self.label,
            children=[
                ui.Text(count),
                ui.Button("+1", color="primary", on_click=increment),
            ],
        )

page = ui.Page(
    ui.Hero(title="Welcome"),
    FeatureCard("Analysis"),
    CounterPanel("Counter"),
)
```

## See also

- [Tutorial 02 — Components](../tutorial/02-components.md)
- [UI components](ui-components.md)
- [State](state.md)
