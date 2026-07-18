from ourui import State, server, ui

source = State("print(1)")
preview = State("<!DOCTYPE html><html><body>hi</body></html>")


@server
def run(**payload: object) -> str:
    return "ok"


page = ui.Page(
    ui.Input("source", type="textarea", bind=source),
    ui.Button("Run", on_click=run),
    ui.Frame(bind=preview, title="Result"),
)
