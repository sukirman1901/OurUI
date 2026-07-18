from ourui import Component, State, server, ui

theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")

count = State(0)


@server
def get_started() -> dict[str, str]:
    return {"message": "Welcome from OurUI server"}


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
    ui.Hero(
        title="Welcome",
        subtitle="Build SaaS in Python",
        cta=ui.Button("Get Started", color="primary", on_click=get_started),
    ),
    ui.Section(
        title="Features",
        children=[
            FeatureCard("Analysis"),
            FeatureCard("Realtime"),
        ],
    ),
    CounterPanel("Counter"),
)
