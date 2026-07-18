"""Enterprise Kit — AI console shell (textarea + Code bind + server echo)."""

from ourui import State, server, ui

prompt = State("Summarize the quarterly report.")
output = State("")


@server
def run_echo(payload: dict | None = None):
    data = payload or {}
    text = str(data.get("prompt") or prompt.get() or "")
    prompt.set(text)
    # Template: replace with your model gateway; OurUI only hosts the UI + RPC.
    echoed = f"# Echo\n\n{text}" if text.strip() else "(empty prompt)"
    output.set(echoed)
    return {"prompt": prompt.get(), "output": output.get()}


page = ui.Page(
    ui.Nav(
        brand=ui.Text("Acme AI Console"),
        items=[ui.Link("Console", href="/")],
    ),
    ui.Hero(
        title="Console",
        subtitle="Enterprise Kit — textarea Input + Code bind + @server echo.",
    ),
    ui.Form(
        ui.Input(
            name="prompt",
            label="Prompt",
            type="textarea",
            bind=prompt,
            placeholder="Ask something…",
        ),
        ui.Button("Run", color="primary"),
        on_submit=run_echo,
    ),
    ui.Section(
        title="Output",
        children=[ui.Code(bind=output)],
    ),
)
