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
