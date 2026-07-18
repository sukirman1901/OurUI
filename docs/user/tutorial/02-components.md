# Tutorial 02 — Components

## Goal

Reuse UI in two ways: a simple **function component** and a **`Component` class** with a `build()` method.

## Code

**`examples/tutorial/02_components.py`**

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
    ui.Hero(title="Components"),
    FeatureCard("Function component"),
    Banner("Class component"),
)
```

Run:

```bash
ourui serve examples/tutorial/02_components.py
```

## What you learned

- **Function components** are plain Python functions that take props and return a `ui.*` node (here, `ui.Card`).
- **Class components** subclass `Component`, store props on `self`, and implement **`build()`** to return the UI tree.
- Compose both styles inside **`ui.Page`** like any other node.
- Prefer functions for leaf widgets; use classes when you need instance state or a clearer object boundary before adding `State` in the next step.

## Next

- [Tutorial 03 — State and server](03-state-and-server.md)
