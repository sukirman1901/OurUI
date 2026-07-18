# LSP and editor setup

OurUI ships a lightweight **Language Server Protocol (LSP)** for authoring Python UI modules. Run it over **stdio** — editors spawn **`ourui lsp`** as a custom language server.

## Start the server

From a shell (with OurUI installed in your active environment):

```bash
ourui lsp
```

The process reads JSON-RPC messages on stdin and writes responses on stdout. Do not run it in a terminal for daily editing — configure your editor to launch this command instead.

Server info reported on initialize: **`ourui-lsp`** (package version matches `ourui`, currently **1.11.1**). Completions cover `ui.*` kinds, color tokens, and common style intent values (`width=`, `gap=`, …).

## What you get

| Feature | Behavior |
|---------|----------|
| **Completions** | After `ui.` — `Page`, `Hero`, `Section`, `Button`, `Text`, `Card`, `Grid`, `Theme` |
| **Top-level completions** | `State`, `server`, `Component` at line start |
| **Token completions** | Color token names inside `color=`, `variant=`, `bg=`, and `ui.Theme(...)` keyword arguments |
| **Hover** | Documentation for `ui.<Component>` identifiers |

Completions for design tokens map to **`--ourui-*`** CSS variables (for example `primary` → `var(--ourui-primary)`).

Trigger character: **`.`** (for `ui.Page`, `ui.Hero`, etc.).

## Editor configuration

Use the **`ourui lsp`** command from the same Python environment where OurUI is installed (your project venv). Examples below assume the venv binary is on the path or referenced explicitly.

### VS Code / Cursor

Install a Python LSP client extension if needed, then add a **custom language server** or use **`settings.json`** with a generic LSP extension that supports arbitrary stdio servers.

Minimal pattern (extension-dependent):

```json
{
  "ourui.languageServerPath": "${workspaceFolder}/.venv/bin/ourui",
  "ourui.languageServerArgs": ["lsp"]
}
```

If your LSP extension expects a single executable, point it at:

```text
/path/to/.venv/bin/ourui lsp
```

Ensure **`python.analysis`** or Pyright does not conflict — OurUI LSP complements Python tooling; it does not replace type checking.

### Neovim (nvim-lspconfig-style)

```lua
local cmd = vim.fn.exepath("ourui")
if cmd ~= "" then
  vim.lsp.start({
    name = "ourui",
    cmd = { cmd, "lsp" },
    root_dir = vim.fs.dirname(vim.fs.find({ "app.py", "pyproject.toml" }, { upward = true })[1]),
    filetypes = { "python" },
  })
end
```

Adjust **`root_dir`** and **`filetypes`** to match your project. The server syncs open Python buffers via **`textDocument/didOpen`** and **`didChange`**.

### Other editors

Any editor with **custom LSP over stdio** support can use:

| Setting | Value |
|---------|--------|
| Command | `ourui` (full path to venv binary recommended) |
| Arguments | `lsp` |
| Transport | stdio |
| Language / file type | Python (`.py`) |

## Verify it works

1. Open an OurUI module (for example `examples/tutorial/01_page.py`).
2. Type `ui.` and request completions — you should see `Page`, `Hero`, etc.
3. Hover over `ui.Hero` — a short doc string should appear.

If completions are empty, confirm the editor launched **`ourui lsp`** from the venv where **`pip install -e packages/ourui`** was run.

## Limitations (P0)

- Completions are **OurUI-specific** — not full Python IntelliSense.
- No go-to-definition or diagnostics for general Python errors.
- Token completions apply in known patterns (`color="..."`, `ui.Theme(primary="...")`, etc.).

For compiler output beyond the editor, use [Debugging with dump](debugging-with-dump.md).

## See also

- [Getting started](../getting-started.md) — install OurUI in a venv
- [Reference: CLI](../reference/cli.md) — `ourui lsp` entry
- [Tutorial 05 — Theme and tokens](../tutorial/05-theme-tokens.md) — `ui.Theme` and color tokens
