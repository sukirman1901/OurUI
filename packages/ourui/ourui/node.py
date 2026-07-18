from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceSpan:
    path: str
    start_line: int
    start_col: int
    end_line: int
    end_col: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Node:
    id: str
    kind: str
    span: SourceSpan
    attributes: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    children: list[str] = field(default_factory=list)
    provenance: list[str] = field(default_factory=list)
    revision: int = 0
    generation: int = 0
    hash: str = ""

    def compute_hash(self) -> str:
        payload = {
            "kind": self.kind,
            "attributes": self.attributes,
            "children": self.children,
            "provenance": self.provenance,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def with_hash(self) -> Node:
        self.hash = self.compute_hash()
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "span": self.span.to_dict(),
            "attributes": self.attributes,
            "metadata": self.metadata,
            "children": list(self.children),
            "provenance": list(self.provenance),
            "revision": self.revision,
            "generation": self.generation,
            "hash": self.hash or self.compute_hash(),
        }


INTENT_KINDS = frozenset({"Page", "Hero", "Section", "Shell"})
PRESENTATION_KINDS = frozenset({"Button", "Text", "Card", "Grid", "Link"})
KNOWN_KINDS = INTENT_KINDS | PRESENTATION_KINDS

# Authoring layout= intents (emit as shell classes; not Tailwind utilities)
SHELL_LAYOUT_INTENTS = frozenset({"stack", "row", "split-3", "grid"})

THEME_ATTR_KEYS = frozenset({"variant", "color", "bg", "theme"})
